import copy
import typing
from functools import partial

from deka_dubbo.utils.get_logger import get_default_logger, Logger
from deka_dubbo.dubbo_config import BoostDecoratorDefaultParams, RabbitmqConfig, RedisConfig, BoostDecoratorParams
from deka_dubbo.helpers import run_consumer_with_multi_process
from deka_dubbo.consumers.base_consumer import AbstractConsumer, ConsumersManager
from deka_dubbo.factories.consumer_factory import get_consumer
from deka_dubbo.constant import BrokerEnum, ConcurrentModeEnum
from deka_dubbo.publishers.base_publisher import AbstractPublisher


class _Undefined:
    pass


def boost(queue_name, *,
          logger: typing.Callable = _Undefined,
          consumer_function_decorator: typing.Callable = _Undefined,
          function_timeout: float = _Undefined,
          concurrent_num: int = _Undefined,
          specify_concurrent_pool=_Undefined,
          specify_async_loop=_Undefined,
          concurrent_mode: int = _Undefined,
          max_retry_times: int = _Undefined,
          log_level: int = _Undefined,
          is_print_detail_exception: bool = _Undefined,
          is_show_message_get_from_broker: bool = _Undefined,
          qps: float = _Undefined,
          is_using_distributed_frequency_control: bool = _Undefined,
          msg_expire_seconds: float = _Undefined,
          is_send_consumer_heartbeat_to_redis: bool = _Undefined,
          logger_prefix: str = _Undefined,
          create_logger_file: bool = _Undefined,
          do_task_filtering: bool = _Undefined,
          task_filtering_expire_seconds: float = _Undefined,
          schedule_tasks_on_main_thread: bool = _Undefined,
          is_using_rpc_mode: bool = _Undefined,
          broker_exclusive_config: dict = _Undefined,
          broker_kind: int = _Undefined,):
    """
    :param logger: 日志对象
    :param queue_name: 队列名字。
    :param consumer_function_decorator: 函数的装饰器。
    :param function_timeout: 超时秒数, 函数运行超过这个时间，则自动杀死函数。为 0 是不限制。设置后代码性能会变差，非必要不要轻易设置
    :param concurrent_num: 并发数量
    # 如果设置了qps，并且 concurrent_num 是默认的50，会自动开500并发，由于是采用的智能线程池任务少的时候不会真开那么多线程而且会自动缩小线程数量。
    # 由于有很好用的qps 控制运行频率和智能扩大缩小的线程池，此框架建议不需要理会和设置并发数量只需要关心qps就行了，框架的并发是自适应并发数量。
    :param specify_concurrent_pool: 使用指定的线程池(协程池)，可以多个消费者共使用一个线程池，不为None的时候，threads_num失效
    :param specify_async_loop: 指定的async的loop循环，设置并发模式为async才能起作用
    :param concurrent_mode: 并发模式  1.线程(ConcurrentModeEnum.THREADING)        2.gevent(ConcurrentModeEnum.GEVENT)
                                     3.eventlet(ConcurrentModeEnum.EVENTLET)    4.asyncio(ConcurrentModeEnum.ASYNC)
                                     5.单线程(ConcurrentModeEnum.SINGLE_THREAD)
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
    :param schedule_tasks_on_main_thread:直接在主线程调度任务，意味着不能在当前主线程开启同时开启两个消费者，fun.consume()就阻塞了，这之后的代码不会运行
    :param is_using_rpc_mode: 是否使用rpc模式，可以在发布端获取消费端的结果回调，但消耗一定性能，使用async_result.result时候会等待阻塞住当前线程
    :param broker_exclusive_config: 加上不同种类中间件的非通用配置，不同中间件独有的配置，不是所有中间件都兼容的配置
    :param broker_kind: 中间件种类
    :return:
    """
    consumer_init_params_include_boost_decorator_default_params = copy.copy(locals())
    consumer_init_params0 = copy.copy(consumer_init_params_include_boost_decorator_default_params)
    # consumer_init_params0.pop('boost_decorator_default_params')
    consumer_init_params = copy.copy(consumer_init_params0)
    boost_decorator_default_params = BoostDecoratorDefaultParams()
    for k, v in consumer_init_params0.items():
        if v == _Undefined:
            consumer_init_params[k] = boost_decorator_default_params[k]
    logger = consumer_init_params.pop('logger')
    Logger.logger = logger

    def _deco(func):
        func.init_params = consumer_init_params
        consumer = get_consumer(consuming_function=func, **consumer_init_params)
        func.is_decorated_as_consume_function = True
        func.consumer = consumer
        func.queue_name = queue_name

        func.publisher = consumer.publisher_of_same_queue
        func.publish = func.pub = func.apply_async = consumer.publisher_of_same_queue.publish
        func.push = func.delay = consumer.publisher_of_same_queue.push
        func.clear = func.clear_queue = consumer.publisher_of_same_queue.clear

        func.start_consuming_message = func.consume = func.start = consumer.start_consumer_message
        func.multi_process_start = func.multi_process_consume = partial(run_consumer_with_multi_process, func)
        return func

    return _deco
