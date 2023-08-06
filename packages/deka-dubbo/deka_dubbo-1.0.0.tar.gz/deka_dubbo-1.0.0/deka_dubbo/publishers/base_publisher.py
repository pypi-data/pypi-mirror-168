import abc
import atexit
import copy
import datetime
import inspect
import json
import time
import typing
import uuid
from threading import Lock
from typing import Callable
from functools import wraps

import amqpstorm

from deka_dubbo.dubbo_config import RedisDefaultConfig
from deka_dubbo.utils import decorators
from deka_dubbo.utils.get_logger import get_default_logger
from deka_dubbo.utils.redis_manager import RedisMixin
from deka_dubbo.concurrent_pool import ThreadPoolExecutorShrinkAble


class HasNotAsyncResult(Exception):
    pass


class AsyncResult(RedisMixin):
    callback_run_executor = ThreadPoolExecutorShrinkAble(200)

    def __init__(self, task_id, timeout=120):
        self.task_id = task_id
        self.timeout = timeout
        self._has_pop = False
        self._status_and_result = None

    def set_timeout(self, timeout=60):
        self.timeout = timeout
        return self

    def is_pending(self):
        return not self.redis_db_filter_and_rpc_result.exists(self.task_id)

    @property
    def status_and_result(self):
        if not self._has_pop:
            redis_value = self.redis_db_filter_and_rpc_result(self.task_id, self.timeout)
            self._has_pop = True
            if redis_value is not None:
                status_and_result_str = redis_value[1]
                self._status_and_result = json.loads(status_and_result_str)
                self.redis_db_filter_and_rpc_result.lpush(self.task_id, status_and_result_str)
                self.redis_db_filter_and_rpc_result.expire(self.task_id, 600)
                return self._status_and_result
            return None
        return self._status_and_result

    def get(self):
        if self.status_and_result is not None:
            return self.status_and_result['result']
        else:
            raise HasNotAsyncResult

    @property
    def result(self):
        return self.get()

    def is_success(self):
        return self.status_and_result['success']

    def _run_callback_func(self, callback_func):
        callback_func(self.status_and_result)

    def set_callback(self, callback_func: typing.Callable):
        """
        :param callback_func: 函数结果回调函数，使回调函数自动在线程池中并发运行
        :return:
        """
        self.callback_run_executor.submit(self._run_callback_func, callback_func)


RedisAsyncResult = AsyncResult  # 别名


class PriorityConsumingControlConfig(object):
    """
    为每个独立的任务设置控制参数，和函数一起发布到中间件。
    例如消费为add函数，可以每个独立的任务设置不同的超时时间，不同的重复次数，是否使用rpc模式。这里的配置优先，可以覆盖生成消费者时候的配置
    """
    def __init__(self, function_timeout: float = None, max_retry_times: int = None,
                 is_print_detail_exception: bool = None,
                 msg_expire_seconds: int = None,
                 is_using_rpc_mode: bool = None):
        """
        :param function_timeout:  超时杀死
        :param max_retry_times:   最大重启次数
        :param is_print_detail_exception: 是否打印详细的堆栈错误
        :param msg_expire_seconds: 消息过期时间
        """
        self.function_timeout = function_timeout
        self.max_retry_times = max_retry_times
        self.is_print_detail_exception = is_print_detail_exception
        self.msg_expire_seconds = msg_expire_seconds
        self.is_using_rpc_mode = is_using_rpc_mode

    def to_dict(self):
        priority_consuming_control_config_dict = {k: v for k, v in self.__dict__.items() if v is not None}
        return priority_consuming_control_config_dict


class PublishParamsChecker(object):
    """发布的任务的函数参数检查，使发布的任务在消费时候不会出现低级错误"""

    def __init__(self, func: Callable):
        spec = inspect.getfullargspec(func)
        self.all_arg_name = spec.args
        self.all_arg_name_set = set(spec.args)

        if spec.defaults:
            len_defaults_args = len(spec.defaults)
            # 位置参数列表
            self.position_arg_name_list = spec.args[0:-len_defaults_args]
            self.position_arg_name_set = set(self.position_arg_name_list)
            # 关键字参数列表
            self.keyword_arg_name_list = spec.args[-len_defaults_args:]
            self.keyword_arg_name_set = set(self.keyword_arg_name_list)
        else:
            self.position_arg_name_list = spec.args
            self.position_arg_name_set = set(self.position_arg_name_list)
            self.keyword_arg_name_list = []
            self.keyword_arg_name_set = {}

    def check_params(self, publish_params: dict):
        publish_params_keys_set = set(publish_params.keys())
        if publish_params_keys_set.issubset(self.all_arg_name_set) and \
           publish_params_keys_set.issuperset(self.position_arg_name_set):
            return True
        else:
            raise ValueError(f'你发布的参数不正确，你发布的任务的所有键是 {publish_params_keys_set}， '
                             f'必须是 {self.all_arg_name_set} 的子集， 必须是 {self.position_arg_name_set} 的超集')


class AbstractPublisher(metaclass=abc.ABCMeta):

    def __init__(self, queue_name, *, logger=get_default_logger(), log_level_int=10, log_prefix='', log_write_to_file=False,
                 clear_queue_within_init=False, is_add_publish_time=True, consuming_function: Callable = None,
                 broker_kind: int = None):
        """
        :param queue_name: 队列名字
        :param logger: 日志对象
        :param log_level_int:  日志等级
        :param log_prefix:  日志前缀
        :param log_write_to_file: 是否将日志写入文件中
        :param clear_queue_within_init: 清除当前队列
        :param is_add_publish_time: 是否添加发布时间，默认添加
        :param consuming_function: 消费函数
        :param broker_kind: 中间件种类
        :return:
        """
        self.queue_name = queue_name
        self.log_level_int = log_level_int

        if log_prefix != '':
            log_prefix += '--'
        self.log_prefix = log_prefix

        self.log_write_to_file = log_write_to_file
        # logger_name = f'{log_prefix}{self.__class__.__name__}--{queue_name}'

        # self.logger = log_manager.get_builder().set_log_level_int(log_level_int)\
        #                                        .set_log_write_to_file(log_write_to_file)\
        #                                        .set_log_filename(logger_name).builder()
        self.logger = logger
        self.clear_queue_within_init = clear_queue_within_init
        self.is_add_publish_time = is_add_publish_time
        self.broker_kind = broker_kind

        self.publish_params_checker = PublishParamsChecker(consuming_function) if consuming_function else None

        self.has_init_broker = 0
        self.lock_for_count = Lock()
        self.current_time = None
        self.count_per_minute = None
        self.init_count()
        self.custom_init()
        self.logger.info(f'{self.__class__} 被实例化了')
        self.publish_msg_num_total = 0
        self.__init_time = time.time()
        atexit.register(self._at_exit)
        if clear_queue_within_init:
            self.clear()

    def init_count(self):
        self.current_time = time.time()
        self.count_per_minute = 0

    def custom_init(self):
        pass

    def publish(self, msg: typing.Union[str, dict], task_id=None,
                priority_control_config: PriorityConsumingControlConfig = None):
        """
        :param msg: 函数的入参字典或者字典转json， 例如消费函数是 def add(x, y)， 你就发布{"x":1, "y":2}
        :param task_id: 可以指定task_id, 也可以不指定就随机生产uuid
        :param priority_control_config: 优先级配置，消息可以携带优先级配置，覆盖boost的配置
        :return:
        """
        if isinstance(msg, str):
            msg = json.loads(msg)
        msg_function_kw = copy.copy(msg)
        if self.publish_params_checker:
            self.publish_params_checker.check_params(msg)
        task_id = task_id or f'{self.queue_name}_result:{uuid.uuid4()}'
        msg['extra'] = extra_params = {'task_id': task_id, 'publish_time': round(time.time(), 4),
                                       'publish_time_format': time.strftime('%Y-%m-%d %H:%M:%S')}
        if priority_control_config:
            extra_params.update(priority_control_config.to_dict())
        t_start = time.time()
        decorators.handle_exception(retry_times=10, is_show_error=True, time_sleep=0.1)\
                                   (self.concrete_realization_publish)(json.dumps(msg, ensure_ascii=False))
        self.logger.debug(f'向{self.queue_name}队列，推送消息， 耗时{round(time.time() - t_start, 4)}秒 {msg_function_kw}')
        with self.lock_for_count:
            self.count_per_minute += 1
            self.publish_msg_num_total += 1
            if time.time() - self.current_time > 10:
                self.logger.info(f'10秒内推送了 {self.count_per_minute} 条消息，累计推送了 {self.publish_msg_num_total} 条消息到'
                                 f' {self.queue_name} 队列中')
                self.init_count()

        return AsyncResult(task_id)

    def push(self, *func_args, **func_kwargs):
        """
        简写，只支持传递消息函数的本身参数，不支持priority_control_config参数。
        类似于 publish 和 push 的关系 类似 apply_async 和 delay 的关系。前者更强大，后者更简略
        :param func_args:
        :param func_kwargs:
        :return:
        """
        msg_dict = func_kwargs

        for index, arg in enumerate(func_args):
            msg_dict[self.publish_params_checker.all_arg_name[index]] = arg
        return self.publish(msg_dict)

    delay = push

    @abc.abstractmethod
    def concrete_realization_publish(self, msg: str):
        raise NotImplementedError

    @abc.abstractmethod
    def clear(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_message_count(self):
        raise NotImplementedError

    @abc.abstractmethod
    def close(self):
        raise NotImplementedError

    def _at_exit(self):
        self.logger.warning(
            f'程序关闭前，{round(time.time() - self.__init_time)} 秒内，'
            f'累计推送了 {self.publish_msg_num_total} 条消息 到 {self.queue_name} 中')


def deco_mq_conn_error(f):
    @wraps(f)
    def _deco_mq_conn_error(self, *args, **kwargs):
        if not self.has_init_broker:
            self.logger.warning(f'对象的方法 【{f.__name__}】 首次使用 进行初始化执行 init_broker 方法')
            self.init_broker()
            self.has_init_broker = 1
            return f(self, *args, **kwargs)
        # noinspection PyBroadException
        try:
            return f(self, *args, **kwargs)
        except amqpstorm.AMQPError as e:  # except Exception as e:   # 现在装饰器用到了绝大多出地方，单个异常类型不行。ex
            self.logger.error(f'中间件链接出错,方法 {f.__name__}  出错 ，{e}')
            self.init_broker()
            return f(self, *args, **kwargs)
        except Exception as e:
            self.logger.critical(e, exc_info=True)

    return _deco_mq_conn_error
