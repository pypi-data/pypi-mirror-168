import abc
import asyncio
import atexit
import copy
import datetime
import json
import logging
import os
import socket
import sys
import threading
import time
import traceback
import typing
import uuid
from threading import Thread
from functools import wraps

from deka_dubbo.concurrent_pool.async_pool_executor import AsyncPoolExecutor
from deka_dubbo.concurrent_pool.single_thread_executor import SoloExecutor
from deka_dubbo.constant import ConcurrentModeEnum
from deka_dubbo.consumers.redis_filter import RedisFilter, RedisImpermanencyFilter
from deka_dubbo.utils.get_logger import get_default_logger, Logger
from deka_dubbo.factories.publisher_factory import get_publisher
from deka_dubbo.utils import decorators, time_util
from deka_dubbo.utils.get_host_ip import computer_ip, computer_name
from deka_dubbo.utils.redis_manager import RedisMixin
from deka_dubbo.concurrent_pool.custom_threadpool_executor import ThreadPoolExecutorShrinkAble
from deka_dubbo.concurrent_pool.async_helper import simple_run_in_executor


def delete_keys_and_return_new_dict(dictx: dict, keys: list = None):
    dict_new = copy.copy(dictx)
    keys = ['publish_time', 'publish_time_format', 'extra'] if keys is None else keys
    for dict_key in keys:
        try:
            dict_new.pop(dict_key)
        except KeyError:
            pass
    return dict_new


def get_publish_time(paramsx: dict):
    return paramsx.get('extra', {}).get('publish_time', None) or paramsx.get('publish_time', None)


class FunctionResultStatus(object):
    host_name = socket.gethostname()
    host_process = f'{host_name} - {os.getpid()}'
    script_name_long = sys.argv[0]
    script_name = script_name_long.split('/')[-1].split('\\')[-1]

    def __init__(self, queue_name: str, function_name: str, msg_dict: dict):
        self.queue_name = queue_name
        self.function = function_name
        self.msg_dict = msg_dict
        self.task_id = self.msg_dict.get('extra', {}).get('task_id', '')
        self.process_id = os.getpid()
        self.thread_id = threading.get_ident()
        self.publish_time = publish_time = get_publish_time(msg_dict)
        if publish_time:
            self.publish_time_str = time_util.DatetimeConverter(publish_time).datetime_str
        function_params = delete_keys_and_return_new_dict(msg_dict, )
        self.params = function_params
        self.params_str = json.dumps(function_params, ensure_ascii=False)
        self.result = None
        self.run_times = 0
        self.exception = None
        self.time_start = time.time()
        self.time_cost = None
        self.time_end = None
        self.success = False
        self.total_thread = threading.active_count()
        self.has_requeue = False

    def get_status_dict(self, without_datetime_obj=False):
        self.time_end = time.time()
        self.time_cost = round(self.time_end - self.time_start, 3)
        item = self.__dict__
        item['host_name'] = self.host_name
        item['host_process'] = self.host_process
        item['script_name'] = self.script_name
        item['script_name_long'] = self.script_name_long
        datetime_str = time_util.DatetimeConverter().datetime_str
        try:
            json.dumps(item['result'])
        except TypeError:
            item['result'] = str(item['result'])[:1000]
        item.update({'insert_time_str': datetime_str,
                     'insert_minutes': datetime_str[:-3],
                     })
        if not without_datetime_obj:
            item.update({'insert_time': datetime.datetime.now(),
                         'utime': datetime.datetime.utcnow(),
                         })
        else:
            item = delete_keys_and_return_new_dict(item, ['insert_time', 'utime'])
        item['_id'] = self.task_id or str(uuid.uuid4())
        return item


class ConsumersManager:

    schedual_thread_to_be_join = []
    global_concurrent_mode = None
    schedual_task_always_use_thread = False
    _has_show_consumer_info = False

    @staticmethod
    def get_concurrent_name_by_concurrent_mode(concurrent_mode):
        if concurrent_mode == ConcurrentModeEnum.THREADING:
            return 'thread'
        elif concurrent_mode == ConcurrentModeEnum.ASYNC:
            return 'async'
        elif concurrent_mode == ConcurrentModeEnum.SINGLE_THREAD:
            return 'single_thread'

    @classmethod
    def join_all_consumer_schedual_task_thread(cls):
        """实现这个主要是为了兼容 linux 和 win , 在开启多进程时兼容"""
        if cls.schedual_task_always_use_thread:
            for t in cls.schedual_thread_to_be_join:
                t.join()

        else:
            if cls.global_concurrent_mode in [ConcurrentModeEnum.THREADING, ConcurrentModeEnum.ASYNC]:
                for t in cls.schedual_thread_to_be_join:
                    t.join()


# noinspection DuplicatedCode
class AbstractConsumer(metaclass=abc.ABCMeta):
    """
    所有消费者的抽象基类
    """
    BROKER_KIND = None

    def __init__(self, queue_name, *,
                 consuming_function: typing.Callable = None,
                 consumer_function_decorator: typing.Callable = None,
                 function_timeout: float = 0,
                 concurrent_num: int = 50,
                 specify_concurrent_pool=None,
                 specify_async_loop=None,
                 concurrent_mode: int = ConcurrentModeEnum.THREADING,
                 max_retry_times: int = 3,
                 log_level: int = 10,
                 is_print_detail_exception: bool = True,
                 is_show_message_get_from_broker: bool = False,
                 qps: float = 0,
                 is_using_distributed_frequency_control: bool = False,
                 msg_expire_seconds: float = 0,
                 is_send_consumer_heartbeat_to_redis: bool = False,
                 logger_prefix: str = '',
                 create_logger_file: bool = True,
                 do_task_filtering: bool = False,
                 task_filtering_expire_seconds: float = 0,
                 schedule_tasks_on_main_thread: bool = False,
                 is_using_rpc_mode: bool = False,
                 broker_exclusive_config: dict = None):
        """
           :param queue_name: 队列名字。
           :param consuming_function: 处理消息的函数。
           :param consumer_function_decorator: 函数的装饰器。
           :param function_timeout: 超时秒数, 函数运行超过这个时间，则自动杀死函数。为 0 是不限制。设置后代码性能会变差，非必要不要轻易设置
           :param concurrent_num: 并发数量
           # 如果设置了qps，并且 concurrent_num 是默认的50，会自动开500并发，由于是采用的智能线程池任务少的时候不会真开那么多线程而且会自动缩小线程数量。
           # 由于有很好用的qps 控制运行频率和智能扩大缩小的线程池，此框架建议不需要理会和设置并发数量只需要关心qps就行了，框架的并发是自适应并发数量。
           :param specify_concurrent_pool: 使用指定的线程池(协程池)，可以多个消费者共使用一个线程池，不为None的时候，threads_num失效
           :param specify_async_loop: 指定的async的loop循环，设置并发模式为async才能起作用
           :param concurrent_mode: 并发模式  1.线程(ConcurrentModeEnum.THREADING)      2.asyncio(ConcurrentModeEnum.ASYNC)
                                            3.单线程(ConcurrentModeEnum.SINGLE_THREAD)
           :param max_retry_times: 最大重启次数，当函数发生错误，立即重试运行n次，对一些特殊不稳定情况会有效果
           :param log_level: 设置日志级别， 从低到高为  logging.DEBUG(10) logging.INFO(20) logging.WARNING(30) logging.ERROR(40) logging.CRITICAL(50)
           :param is_print_detail_exception: 是否打印详细的堆栈错误，为 0 则打印简略的错误
           :param is_show_message_get_from_broker: 从中间件取出消息时候打印显示出来
           :param qps: 指定 1 秒内的函数执行次数，例如可以是小数0.01代表每100秒执行一次，也可以是50代表1秒执行50次，为0则不控频
           :param is_using_distributed_frequency_control:是否使用分布式控频（依赖redis统计消费者数量，然后频率平分），默认只对当前实例化的消费者控频有效
           :param msg_expire_seconds: 消息过期时间，为0永不过期，表示xx秒之前发布的任务，如果现在才轮到消费，则丢弃任务
           :param is_send_consumer_heartbeat_to_redis: 是否将发布者的心跳发送到redis，有些功能的实现需要统计活跃消费者，因为有的中间件不是真mq
           :param logger_prefix: 日志前缀，可使用不同的消费者生成不同的日志前缀
           :param create_logger_file: 是否创建日志文件
           :param do_task_filtering: 是否执行基于函数参数的任务过滤
           :param task_filtering_expire_seconds: 任务过滤的失效期
           :param schedule_tasks_on_main_thread:
           :param is_using_rpc_mode: 直接在主线程调度任务，意味着不能在当前主线程开启同时开启两个消费者，fun.consume()就阻塞了，这之后的代码不会运行
           :return:
           """
        self.init_params = copy.copy(locals())
        self.init_params.pop('self')
        self.init_params['broker_kind'] = self.__class__.BROKER_KIND

        current_queue_info_dict = copy.copy(self.init_params)
        current_queue_info_dict['consuming_function'] = str(consuming_function)
        current_queue_info_dict['class_name'] = self.__class__.__name__
        concurrent_name = ConsumersManager.get_concurrent_name_by_concurrent_mode(concurrent_mode)
        current_queue_info_dict['concurrent_name'] = concurrent_name

        self.logger = Logger.logger
        self.queue_name = queue_name
        if consuming_function is None:
            raise ValueError('必须传 consuming_function 参数')
        self.consuming_function = consuming_function
        self.consumer_function_decorator = consumer_function_decorator
        self.function_timeout = function_timeout

        # 如果设置了,并且concurrent_num是默认的50,会自动开了500并发。
        if qps != 0 and concurrent_num == 50:
            self.concurrent_num = 500
        else:
            self.concurrent_num = concurrent_num

        self.specify_concurrent_pool = specify_concurrent_pool
        self.specify_async_loop = specify_async_loop
        self.concurrent_pool = None
        self.concurrent_mode = concurrent_mode
        if self.concurrent_mode not in (1, 2, 3):
            raise ValueError('设置的并发模式不正确')
        self.concurrent_mode_dispatcher = ConcurrentModeDispatcher(self)
        if self.concurrent_mode == ConcurrentModeEnum.ASYNC:
            self._run = self._async_run

        self.max_retry_times = max_retry_times
        self.is_print_detail_exception = is_print_detail_exception
        self.is_show_message_get_from_broker = is_show_message_get_from_broker

        self.qps = qps
        # qps 如果等于0， 消费函数则0秒运行一次，表示不控频
        self.msg_schedule_time_intercal = 0 if qps == 0 else 1.0 / qps

        self.is_using_distributed_frequency_control = is_using_distributed_frequency_control
        self.msg_expire_seconds = msg_expire_seconds
        self.is_send_consumer_heartbeat_to_redis = is_send_consumer_heartbeat_to_redis or is_using_distributed_frequency_control

        self.logger_prefix = logger_prefix
        self.log_level = log_level

        self.create_logger_file = create_logger_file
        if logger_prefix != '':
            logger_prefix += '--'
        logger_name = f'{logger_prefix}{self.__class__.__name__}--{queue_name}'
        # log_manager = get_log_manager()
        # self.logger = log_manager.get_builder().set_log_level_int(self.log_level)\
        #                                        .set_log_write_to_file(self.create_logger_file)\
        #                                        .set_log_filename(logger_name).builder()

        self.do_task_filtering = do_task_filtering
        self.redis_filter_key_name = f'filter_zset:{queue_name}' if task_filtering_expire_seconds\
                                     else f'filter_set:{queue_name}'
        filter_class = RedisFilter if task_filtering_expire_seconds == 0 else RedisImpermanencyFilter
        self.redis_filter = filter_class(self.redis_filter_key_name, task_filtering_expire_seconds)

        # self.is_do_not_run_by_specify_time_effect = is_do_not_run_by_specify_time_effect
        # self.do_not_run_by_specify_time = do_not_run_by_specify_time
        self.schedule_tasks_on_main_thread = schedule_tasks_on_main_thread

        self.is_using_rpc_mode = is_using_rpc_mode

        self._publisher_of_same_queue = None

        self.stop_flag = None
        self.pause_flag = None
        self.last_show_pause_log_time = 0
        self.redis_key_stop_flag = f'funboost_stop_flag: {self.queue_name}'
        self.redis_key_pause_flag = f'funboost_pause_flag: {self.queue_name}'

        self.msg_num_in_broker = 0
        self.last_timestamp_print_msg_num = 0
        self.last_timestamp_when_has_task_in_queue = 0

        self.unit_time_for_count = 10  # 每隔多少秒计数，显示单位时间内执行多少次，暂时固定为10秒
        self.execute_task_times_every_unit_time = 0  # 每单位时间执行了多少次
        self.lock_for_count_execute_task_times_every_unit_time = threading.Lock()
        self.current_time_for_execute_task_times_every_unit_time = time.time()
        self.consuming_function_cost_time_total_every_unit_time = 0
        self.last_execute_task_time = time.time()  # 最近一次执行任务的时间

        # 控频要用到的成员变量
        self.last_submit_task_timestamp = 0
        self.last_start_count_qps_timestamp = time.time()
        self.has_execute_times_in_recent_second = 0

        # 消费者标识
        self.consumer_identification = f'{computer_name}_{computer_ip}_' \
                                       f'{time_util.DatetimeConverter().datetime_str.replace(":", "-")}_' \
                                       f'{os.getpid()}'
        self.consumer_identification_map = {'queue_name': self.queue_name,
                                            'computer_name': computer_name,
                                            'computer_ip': computer_ip,
                                            'process_id': os.getpid(),
                                            'consumer_id': id(self),
                                            'consumer_uuid': str(uuid.uuid4()),
                                            'start_datetime_str': time_util.DatetimeConverter().datetime_str,
                                            'start_timestamp': time.time(),
                                            'heartbeat_datetime_str': time_util.DatetimeConverter().datetime_str,
                                            'heartbeat_timestamp': time.time(),
                                            'consumer_function': self.consuming_function.__name__,
                                            }

        atexit.register(self.join_shedual_task_thread)

    @property
    @decorators.synchronized
    def publisher_of_same_queue(self):
        if not self._publisher_of_same_queue:
            self._publisher_of_same_queue = get_publisher(self.queue_name, logger=self.logger, log_level_int=self.log_level,
                                                          log_write_to_file=self.create_logger_file,
                                                          consuming_function=self.consuming_function,
                                                          broker_kind=self.BROKER_KIND)

        return self._publisher_of_same_queue
    # noinspection PyProtectedMember,PyUnresolvedReferences

    @classmethod
    def join_shedual_task_thread(cls):
        ConsumersManager.join_all_consumer_schedual_task_thread()

    @property
    @decorators.synchronized
    def _concurrent_pool(self):
        return self.concurrent_mode_dispatcher.build_pool()

    # noinspection PyAttributeOutsideInit
    def start_consumer_message(self):
        self.logger.warning(f'开始消费 {self.queue_name} 中的消息')

        self.distributed_consumer_statistics = DistributedConsumerStatistics(self)
        if self.is_send_consumer_heartbeat_to_redis:
            self.distributed_consumer_statistics.run()
            self.logger.warning(
                f'启动了分布式环境 使用 redis 的键 heartbeat:{self.queue_name} 统计活跃消费者 ，当前消费者唯一标识为 {self.consumer_identification}')

        self.keep_circulating(10, block=False)(self.check_heartbeat_and_message_count)()

        if self.do_task_filtering:
            self.redis_filter.delete_expire_filter_task_cycle(logger=self.logger)
        if self.schedule_tasks_on_main_thread:
            self.keep_circulating(1)(self.shedual_task)()
        else:
            self.concurrent_mode_dispatcher.schedual_task_with_no_block()

    @abc.abstractmethod
    def shedual_task(self):
        """
        每个子类必须实现这个方法，完成如何从中间件取出消息，并将函数和运行参数添加到工作池
        :return:
        """
        raise NotImplementedError

    def get_priority_conf(self, kw: dict, broker_task_config_key: str):
        broker_task_config = kw['body'].get('extra', {}).get(broker_task_config_key, None)
        if broker_task_config is None:
            return getattr(self, f'{broker_task_config_key}', None)
        else:
            return broker_task_config

    def _run(self, kw: dict,):
        t_start_run_fun = time.time()
        max_retry_times = self.get_priority_conf(kw, 'max_retry_times')
        current_function_result_status = FunctionResultStatus(self.queue_name, self.consuming_function.__name__,
                                                              kw['body'], )
        current_retry_times = 0
        function_only_params = delete_keys_and_return_new_dict(kw['body'])
        for current_retry_times in range(max_retry_times + 1):
            current_function_result_status = self._run_consuming_function_with_confirm_and_retry\
                                                (kw, current_retry_times=current_retry_times,
                                                 function_result_status=FunctionResultStatus
                                                 (self.queue_name, self.consuming_function.__name__, kw['body']), )

            if current_function_result_status.success is True or current_retry_times == max_retry_times or\
               current_function_result_status.has_requeue:
                break
        self.confirm_consume(kw)
        if self.get_priority_conf(kw, 'do_task_filtering'):
            # 函数执行成功后，添加函数的参数排序后的键值对字符串到set中。
            self.redis_filter.add_a_value(function_only_params)
        if current_function_result_status.success is False and current_retry_times == max_retry_times:
            self.logger.critical(
                f'函数 {self.consuming_function.__name__} 达到最大重试次数 {max_retry_times} 后仍然失败'
                f'入参是 {function_only_params}'
            )
        if self.get_priority_conf(kw, 'is_using_rpc_mode'):
            with RedisMixin().redis_db_filter_and_rpc_result.pipeline() as p:
                p.lpush(kw['body']['extra']['task_id'], json.dumps(current_function_result_status.
                                                                   get_status_dict(without_datetime_obj=True)))
                p.expire(kw['body']['extra']['task_id'], 600)
                p.execute()
        with self.lock_for_count_execute_task_times_every_unit_time:
            self.execute_task_times_every_unit_time += 1
            self.consuming_function_cost_time_total_every_unit_time += time.time() - t_start_run_fun
            self.last_execute_task_time = time.time()
            if time.time() - self.current_time_for_execute_task_times_every_unit_time > self.unit_time_for_count:
                average_function_spend_time = round(self.consuming_function_cost_time_total_every_unit_time / self.execute_task_times_every_unit_time, 4)
                msg = f'{self.unit_time_for_count} 秒内执行了 {self.execute_task_times_every_unit_time} 次函数 [ {self.consuming_function.__name__} ],' \
                      f'函数平均运行耗时 {average_function_spend_time} 秒'
                if self.msg_num_in_broker != -1:
                    need_time = time_util.seconds_to_hour_minute_second(self.msg_num_in_broker /
                                                                        (self.execute_task_times_every_unit_time /
                                                                         self.unit_time_for_count) /
                                                                        self.distributed_consumer_statistics.active_consumer_num)
                    msg += f''' ，预计还需要 {need_time}''' + \
                           f''' 时间 才能执行完成 {self.msg_num_in_broker}个剩余的任务'''
                self.logger.info(msg)
                self.current_time_for_execute_task_times_every_unit_time = time.time()
                self.consuming_function_cost_time_total_every_unit_time = 0
                self.execute_task_times_every_unit_time = 0

    def _run_consuming_function_with_confirm_and_retry(self, kw: dict, current_retry_times,
                                                       function_result_status: FunctionResultStatus, ):
        function_only_params = delete_keys_and_return_new_dict(kw['body'])
        t_start = time.time()
        function_result_status.run_times = current_retry_times + 1
        try:
            function_timeout = self.get_priority_conf(kw, 'function_timeout')
            function_run0 = self.consuming_function if self.consumer_function_decorator is None \
                                                    else self.consumer_function_decorator(self.consuming_function)
            function_run = function_run0 if not function_timeout \
                                         else self.concurrent_mode_dispatcher.timeout_deco(function_timeout)(function_run0)
            function_result_status.result = function_run(**function_only_params)
            if asyncio.iscoroutine(function_result_status.result):
                self.logger.critical(f'异步的协程消费函数必须使用 async 并发模式并发,请设置'
                                     f'消费函数 {self.consuming_function.__name__} 的concurrent_mode 为ConcurrentModeEnum.ASYNC')
                # noinspection PyProtectedMember,PyUnresolvedReferences
                os._exit(4)
            function_result_status.success = True
            # log_level = self.get_priority_conf(kw, 'log_level')
            # if log_level is None:
            #     log_level = 10
            # if log_level <= logging.DEBUG:
            result_str_to_be_print = str(function_result_status.result) \
                                         if len(str(function_result_status)) < 100 \
                                         else str(function_result_status.result)[:100] + '  。。。 '
            self.logger.debug(f' 函数 {self.consuming_function.__name__}  '
                              f' 第{current_retry_times + 1}次 运行, 正确了，函数运行时间是 {round(time.time() - t_start, 4)} 秒,入参是 {function_only_params}  '
                              f' 结果是  {result_str_to_be_print}')
        except Exception as e:
            self.logger.error(f'函数 {self.consuming_function.__name__}  第{current_retry_times + 1}次运行发生错误，'
                              f'函数运行时间是 {round(time.time() - t_start, 4)} 秒,\n  入参是  {function_only_params}\n 原因是 {type(e)} {e} ')
            function_result_status.exception = f'{e.__class__.__name__}    {str(e)}'
        return function_result_status

    async def _async_run(self, kw: dict, ):
        t_start_run_fun = time.time()
        max_retry_times = self.get_priority_conf(kw, 'max_retry_times')
        current_function_result_status = FunctionResultStatus(self.queue_name, self.consuming_function.__name__, kw['body'], )
        current_retry_times = 0
        function_only_params = delete_keys_and_return_new_dict(kw['body'])
        for current_retry_times in range(max_retry_times + 1):
            current_function_result_status = await self._async_run_consuming_function_with_confirm_and_retry(kw, current_retry_times=current_retry_times,
                                                                                                             function_result_status=FunctionResultStatus(
                                                                                                                 self.queue_name, self.consuming_function.__name__,
                                                                                                                 kw['body']
                                                                                                             ))
            if current_function_result_status.success is True or current_retry_times == max_retry_times or current_function_result_status.has_requeue:
                break

        await simple_run_in_executor(self.confirm_consume, kw)
        if self.get_priority_conf(kw, 'do_task_filtering'):
            await simple_run_in_executor(self.redis_filter.add_a_value, function_only_params)

        if current_function_result_status.success is False and current_retry_times == max_retry_times:
            self.logger.critical(
                f'函数 {self.consuming_function.__name__} 达到最大重试次数 {self.get_priority_conf(kw, "max_retry_times")} '
                f'后,仍然失败， 入参是  {function_only_params} ')

        if self.get_priority_conf(kw, 'is_using_rpc_mode'):
            def push_result():
                with RedisMixin().redis_db_filter_and_rpc_result.pipeline() as p:
                    p.lpush(kw['body']['extra']['task_id'],
                            json.dumps(current_function_result_status.get_status_dict(without_datetime_obj=True)))
                    p.expire(kw['body']['extra']['task_id'], 600)
                    p.execute()

            await simple_run_in_executor(push_result)

        # 异步执行不存在线程并发，不需要加锁。
        self.execute_task_times_every_unit_time += 1
        self.consuming_function_cost_time_total_every_unit_time += time.time() - t_start_run_fun
        self.last_execute_task_time = time.time()
        if time.time() - self.current_time_for_execute_task_times_every_unit_time > self.unit_time_for_count:
            average_function_spend_time = round(self.consuming_function_cost_time_total_every_unit_time / self.execute_task_times_every_unit_time, 4)
            msg = f'{self.unit_time_for_count} 秒内执行了 {self.execute_task_times_every_unit_time} 次函数 [ {self.consuming_function.__name__} ]' \
                  f'函数平均运行耗时 {average_function_spend_time} 秒'
            # 有的中间件无法统计或实现统计队列剩余数量，统一返回的是-1，不显示这句换
            if self.msg_num_in_broker != -1:
               need_time = time_util.seconds_to_hour_minute_second(self.msg_num_in_broker /
                                                                   (self.execute_task_times_every_unit_time /
                                                                    self.unit_time_for_count) /
                                                                   self.distributed_consumer_statistics.active_consumer_num)
               msg += f''' ，预计还需要 {need_time}''' + \
                      f''' 时间 才能执行完成 {self.msg_num_in_broker}个剩余的任务'''
            self.logger.info(msg)
            self.current_time_for_execute_task_times_every_unit_time = time.time()
            self.consuming_function_cost_time_total_every_unit_time = 0
            self.execute_task_times_every_unit_time = 0

    async def _async_run_consuming_function_with_confirm_and_retry(self, kw:dict, current_retry_times,
                                                                   function_result_status: FunctionResultStatus,):
        function_only_params = delete_keys_and_return_new_dict(kw['body'])
        function_result_status.run_times = current_retry_times + 1
        t_start = time.time()
        try:
            coroutine_obj = self.consuming_function(**function_only_params)
            if not asyncio.iscoroutine(coroutine_obj):
                self.logger.critical(f'当前设置的并发模式为 async 并发模式，但消费函数不是异步协程函数，'
                                     f'请不要把消费函数 {self.consuming_function.__name__} 的 concurrent_mode 设置为 4')
                # noinspection PyProtectedMember,PyUnresolvedReferences
                os._exit(444)
            if self.function_timeout == 0:
                rs = await coroutine_obj
            else:
                rs = await asyncio.wait_for(coroutine_obj, timeout=self.function_timeout)
            function_result_status.result = rs
            function_result_status.success = True
            log_level = self.get_priority_conf(kw, 'log_level')
            if log_level is None:
                log_level = 10
            if log_level <= logging.DEBUG:
                result_str_to_be_print = str(rs)[:100] if len(str(rs)) < 100 else str(rs)[:100] + '  。。。。。  '
                self.logger.debug(f' 函数 {self.consuming_function.__name__}  '
                                  f'第{current_retry_times + 1}次 运行, 正确了，函数运行时间是 {round(time.time() - t_start, 4)} 秒,'
                                  f'入参是 【 {function_only_params} 】 ,结果是 {result_str_to_be_print}  。 {coroutine_obj} ')
        except Exception as e:
            self.logger.error(f'函数 {self.consuming_function.__name__}  第{current_retry_times + 1}次运行发生错误，'
                              f'函数运行时间是 {round(time.time() - t_start, 4)} 秒,\n  入参是  {function_only_params}    \n 原因是 {type(e)} {e} ',
                              exc_info=self.get_priority_conf(kw, 'is_print_detail_exception'))
            function_result_status.exception = f'{e.__class__.__name__}    {str(e)}'
        return function_result_status

    def print_message_get_from_broker(self, broker_name, msg):
        if isinstance(msg, (dict, list)):
            msg = json.dumps(msg, ensure_ascii=False)
        if self.is_show_message_get_from_broker:
            self.logger.debug(f'从 {broker_name} 中间件 的 {self.queue_name} 中取出的消息是 {msg}')

    @abc.abstractmethod
    def requeue(self, kw):
        """重新入队"""
        raise NotImplementedError

    @abc.abstractmethod
    def confirm_consume(self, kw):
        """消费确认"""
        raise NotImplementedError

    def keep_circulating(self, time_sleep=0.001, exit_if_function_run_success=False,
                         is_display_detail_exception=True, block=True):
        """
        间隔一段时间，一直循环运行某个方法的装饰器
        :param time_sleep: 循环间隔的时间
        :param exit_if_function_run_success: 如果成功了就退出循环
        :param is_display_detail_exception:
        :param block: 是否阻塞在当前主线程运行
        :return:
        """

        def _keep_circulating(func):
            @wraps(func)
            def __keep_circulating(*args, **kwargs):
                def ___keep_circulating():
                    while 1:
                        if self.stop_flag == 1:
                            break
                        try:
                            result = func(*args, **kwargs)
                            if exit_if_function_run_success:
                                return result
                        except Exception as e:
                            msg = func.__name__ + '  运行出错\n' + traceback.format_exc(
                                limit=10) if is_display_detail_exception else str(e)
                            self.logger.exception(msg)
                        finally:
                            time.sleep(time_sleep)

                if block:
                    return ___keep_circulating()
                else:
                    threading.Thread(target=___keep_circulating).start()

            return __keep_circulating

        return _keep_circulating

    def check_heartbeat_and_message_count(self):
        """检查心跳和任务数量"""
        self.msg_num_in_broker = self.publisher_of_same_queue.get_message_count()
        if time.time() - self.last_timestamp_print_msg_num > 60:
            if self.msg_num_in_broker != -1:
                self.logger.info(f'队列 [{self.queue_name}] 中还有 [{self.msg_num_in_broker}] 个任务')
            self.last_timestamp_print_msg_num = time.time()
        if self.msg_num_in_broker != 0:
            self.last_timestamp_when_has_task_in_queue = time.time()
        return self.msg_num_in_broker

    def submit_task(self, kw):
        while 1:
            # 这块的代码为支持暂停消费
            if self.pause_flag == 1:
                time.sleep(1)
                if time.time() - self.last_show_pause_log_time > 60:
                    self.logger.warning(f'已设置 {self.queue_name} 队列中的任务为暂停消费')
                    self.last_show_pause_log_time = time.time()
            else:
                break
        function_only_params = delete_keys_and_return_new_dict(kw['body'], )
        if self.get_priority_conf(kw, 'do_task_filtering') and self.redis_filter.check_value_exists(function_only_params):
            self.logger.warning(f'redis 的 [{self.redis_filter_key_name}] 键中过滤任务 {kw["body"]}')
            self.confirm_consume(kw)
            return
        publish_time = get_publish_time(kw['body'])
        msg_expire_seconds_priority = self.get_priority_conf(kw, 'msg_expire_seconds')
        if msg_expire_seconds_priority and time.time() - msg_expire_seconds_priority > publish_time:
            self.logger.warning(
                f'消息发布时戳是 {publish_time} {kw["body"].get("publish_time_format", "")},距离现在 {round(time.time() - publish_time, 4)} 秒 ,'
                f'超过了指定的 {msg_expire_seconds_priority} 秒，丢弃任务')
            self.confirm_consume(kw)
            return 0
        self._concurrent_pool.submit(self._run, kw)

        if self.is_using_distributed_frequency_control:       # 如果是需要分布式控频
            active_num = self.distributed_consumer_statistics.active_consumer_num
            self.frequency_control(self.qps / active_num, self.msg_schedule_time_intercal * active_num)
        else:
            self.frequency_control(self.qps, self.msg_schedule_time_intercal)

    def frequency_control(self, qpsx, msg_schedule_time_intercal):
        # 以下是消费函数qps控制代码。无论是单个消费者控频还是分布式消费控频，都是自己直接计算的。
        if qpsx == 0:
            # 不需要控频的时间，就不需要休眠
            return
        if qpsx <= 5:
            time.sleep(msg_schedule_time_intercal)
        elif 5 < qpsx <= 20:
            time_sleep_for_qps_control = max((msg_schedule_time_intercal - (time.time() -
                                                                            self.last_submit_task_timestamp)) * 0.99, 10 ** -3)
            time.sleep(time_sleep_for_qps_control)
            self.last_submit_task_timestamp = time.time()
        else:
            """基于当前消费者技术的控频，qps很大时候需要使用这种"""
            if time.time() - self.last_start_count_qps_timestamp > 1:
                self.has_execute_times_in_recent_second = 1
                self.last_start_count_qps_timestamp = time.time()
            else:
                self.has_execute_times_in_recent_second += 1
            if self.has_execute_times_in_recent_second >= qpsx:
                time.sleep((1 - (time.time() - self.last_start_count_qps_timestamp)) * 1)


# noinspection PyProtectedMember
class ConcurrentModeDispatcher(object):
    """并发模式调度器"""
    def __init__(self, consumerx: AbstractConsumer):
        self.consumer = consumerx
        self.concurrent_mode = self.consumer.concurrent_mode
        self.timeout_deco = None
        concurrent_name = ConsumersManager.get_concurrent_name_by_concurrent_mode(self.concurrent_mode)
        if self.concurrent_mode in (ConcurrentModeEnum.THREADING, ConcurrentModeEnum.SINGLE_THREAD):
            self.timeout_deco = decorators.timeout
        self.consumer.logger.warning(f'{self.consumer}设置并发模式为{concurrent_name}')

    def schedual_task_with_no_block(self):
        t = Thread(target=self.consumer.keep_circulating(1)(self.consumer.shedual_task))
        ConsumersManager.schedual_thread_to_be_join.append(t)
        t.start()

    def build_pool(self):
        if self.consumer.concurrent_pool is not None:
            return self.consumer.concurrent_pool

        pool_type = None
        if self.concurrent_mode == ConcurrentModeEnum.THREADING:
            pool_type = ThreadPoolExecutorShrinkAble
        elif self.concurrent_mode == ConcurrentModeEnum.ASYNC:
            pool_type = AsyncPoolExecutor
        elif self.concurrent_mode == ConcurrentModeEnum.SINGLE_THREAD:
            pool_type = SoloExecutor

        if self.concurrent_mode == ConcurrentModeEnum.ASYNC:
            self.consumer.concurrent_pool = self.consumer.specify_concurrent_pool if self.consumer.specify_concurrent_pool\
                is not None else pool_type(self.consumer.concurrent_num, loop=self.consumer.specify_async_loop)
        else:
            self.consumer.concurrent_pool = self.consumer.specify_concurrent_pool if self.consumer.specify_concurrent_pool\
                is not None else pool_type(self.consumer.concurrent_num)
        return self.consumer.concurrent_pool


class DistributedConsumerStatistics(RedisMixin):
    """
    为了兼容模拟mq的中间件, 获取一个队列有几个连接活跃消费者数量
    分布式环境中的消费者统计，主要的目的有3点
    1、统计活跃消费者数量用于分布式控频
       获取分布式的消费者数量后，用于分布式qps控频。如果不获取全环境中的消费者数量，则只能用于当前进程中的消费控频
       即使只有一台机器，例如把xx.py启动3次，xx.py的consumer设置qps为10，如果不适用分布式控频，会1秒钟最终运行30次而不是10次。

    2、记录分布式环境中的活跃消费者的所有消费者id。如果消费者id不在此里面说明已掉线或关闭，消息可以重新发布，用于不支持服务端天然消费确认的中间件

    3、从redis中获取停止和暂停状态，以便支持再别的地方发送命令停止或者暂停消费
    """
    def __init__(self, consumer: AbstractConsumer):
        self.consumer_identification = consumer.consumer_identification
        self.consumer_identification_map = consumer.consumer_identification_map
        self.queue_name = consumer.queue_name
        self.consumer = consumer
        self.redis_key_name = f'heartbeat_queue_str:{self.queue_name}'
        self.active_consumer_num = 1
        self.last_show_consumer_num_timestamp = 0

        self._queue_consumer_identification_map_key_name = f'heartbeat_queue_dict: {self.queue_name}'
        self._server_consumer_identification_map_key_name = f'heartbeat_server_dict: {computer_ip}'

    def run(self):
        self.send_heartbeat()
        self.consumer.keep_circulating(10, block=False)(self.send_heartbeat)()

    def send_heartbeat(self):
        results = self.redis_db_frame.smembers(self.redis_key_name)
        with self.redis_db_frame.pipeline() as p:
            for result in results:
                if self.timestamp() - float(result.decode().split('&&')[-1]) > 15 or \
                   self.consumer_identification == result.decode().split('&&')[0]:
                    # 因为这个是10秒钟运行一次，15秒还没更新，那肯定是掉线了，如果消费者本身是自己也先删除
                    p.srem(self.redis_key_name, result)
            p.sadd(self.redis_key_name, f'{self.consumer_identification}&&{self.timestamp()}')
            p.execute()

        self.send_heartbeat_with_dict_value(self._queue_consumer_identification_map_key_name)
        self.send_heartbeat_with_dict_value(self._server_consumer_identification_map_key_name)
        self.show_active_consumer_num()
        self.get_stop_and_pause_flag_from_redis()

    def send_heartbeat_with_dict_value(self, redis_key):
        # 发送当前消费者进程心跳，值是字典，按一个机器或者一个队列运行了哪些进程
        results = self.redis_db_frame.smembers(redis_key)
        with self.redis_db_frame.pipeline() as p:
            for result in results:
                result_dict = json.loads(result)
                if self.timestamp() - result_dict['heartbeat_timestamp'] > 15 \
                        or self.consumer_identification_map['consumer_uuid'] == result_dict['consumer_uuid']:
                    # 因为这个是10秒钟运行一次，15秒还没更新，所以是掉线了。如果消费者本省是自己也先删除
                    p.srem(redis_key, result)

            self.consumer_identification_map['heartbeat_datetime_str'] = time_util.DatetimeConverter().datetime_str
            self.consumer_identification_map['heartbeat_timestamp'] = self.timestamp()
            value = json.dumps(self.consumer_identification_map, sort_keys=True)
            p.sadd(redis_key, value)
            p.execute()

    def show_active_consumer_num(self):
        self.active_consumer_num = self.redis_db_frame.scard(self.redis_key_name) or 1
        if time.time() - self.last_show_consumer_num_timestamp > 600:
            self.consumer.logger.info(f'分布式所有环境中使用 {self.queue_name} 队列的， 一共有 {self.active_consumer_num} 个消费者')
            self.last_show_consumer_num_timestamp = time.time()

    def get_stop_and_pause_flag_from_redis(self):
        stop_flag = self.redis_db_frame.get(self.consumer.redis_key_stop_flag)
        if stop_flag is not None and int(stop_flag) == 1:
            self.consumer.stop_flag = 1
        else:
            self.consumer.stop_flag = 0

        pause_flag = self.redis_db_frame.get(self.consumer.redis_key_pause_flag)
        if pause_flag is not None and int(pause_flag) == 1:
            self.consumer.pause_flag = 1
        else:
            self.consumer.pause_flag = 0
