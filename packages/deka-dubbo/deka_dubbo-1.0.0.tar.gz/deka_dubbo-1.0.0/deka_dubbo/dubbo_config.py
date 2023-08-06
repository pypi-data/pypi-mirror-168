import logging
import typing

from deka_dubbo.utils.simple_data_class import DataClassBase
from deka_dubbo.constant import ConcurrentModeEnum, BrokerEnum
from deka_dubbo.utils.get_logger import get_default_logger


class BoostDecoratorDefaultParams(DataClassBase):
    """
    默认参数配置
    """
    logger = get_default_logger()
    consumer_function_decorator = None
    function_timeout = 0
    concurrent_num = 50
    specify_concurrent_pool = None
    specify_async_loop = None
    concurrent_mode = ConcurrentModeEnum.THREADING
    max_retry_times = 3
    log_level = 10
    is_print_detail_exception: bool = True
    is_show_message_get_from_broker: bool = False
    qps: float = 0
    is_using_distributed_frequency_control: bool = False
    msg_expire_seconds = 0
    is_send_consumer_heartbeat_to_redis: bool = False
    logger_prefix = ''
    create_logger_file: bool = True
    do_task_filtering: bool = False
    task_filtering_expire_seconds = 0
    schedule_tasks_on_main_thread = False
    is_using_rpc_mode: bool = False
    broker_exclusive_config = {}
    broker_kind: int = BrokerEnum.RABBITMQ_AMQPSTORM


class BoostDecoratorParams(object):
    def __init__(self):
        self.boost_default_params = BoostDecoratorDefaultParams

    def set_consumer_function_decorator(self, consumer_function_decorator: typing.Callable):
        self.boost_default_params.consumer_function_decorator = consumer_function_decorator
        return self

    def set_function_timeout(self, function_timeout: int):
        self.boost_default_params.function_timeout = function_timeout
        return self

    def set_concurrent_num(self, concurrent_num: int):
        self.boost_default_params.concurrent_num = concurrent_num
        return self

    def set_specify_concurrent_pool(self, specify_concurrent_pool):
        self.boost_default_params.specify_concurrent_pool = specify_concurrent_pool
        return self

    def set_specify_async_loop(self, specify_async_loop):
        self.boost_default_params.specify_async_loop = specify_async_loop
        return self

    def set_concurrent_mode(self, concurrent_mode: int):
        self.boost_default_params.concurrent_mode = concurrent_mode
        return self

    def set_max_retry_times(self, max_retry_times: int):
        self.boost_default_params.max_retry_times = max_retry_times
        return self

    def set_is_print_detail_exception(self, is_print_detail_exception: bool):
        self.boost_default_params.is_print_detail_exception = is_print_detail_exception
        return self

    def set_is_show_message_get_from_broker(self, is_show_message_get_from_broker: bool):
        self.boost_default_params.is_show_message_get_from_broker = is_show_message_get_from_broker
        return self

    def set_qps(self, qps: float):
        self.boost_default_params.qps = qps
        return self

    def set_is_using_distributed_frequency_control(self, is_using_distributed_frequency_control: bool):
        self.boost_default_params.is_using_distributed_frequency_control = is_using_distributed_frequency_control
        return self

    def set_msg_expire_seconds(self, msg_expire_seconds: float):
        self.boost_default_params.msg_expire_seconds = msg_expire_seconds
        return self

    def set_is_send_consumer_heartbeat_to_redis(self, is_send_consumer_heartbeat_to_redis: bool):
        self.boost_default_params.is_send_consumer_heartbeat_to_redis = is_send_consumer_heartbeat_to_redis
        return self

    def set_do_task_filtering(self, do_task_filtering: bool):
        self.boost_default_params.do_task_filtering = do_task_filtering
        return self

    def set_task_filtering_expire_seconds(self, task_filtering_expire_seconds: float):
        self.boost_default_params.task_filtering_expire_seconds = task_filtering_expire_seconds
        return self

    def set_schedule_tasks_on_main_thread(self, schedule_tasks_on_main_thread: bool):
        self.boost_default_params.schedule_tasks_on_main_thread = schedule_tasks_on_main_thread
        return self

    def set_is_using_rpc_mode(self, is_using_rpc_mode: bool):
        self.boost_default_params.is_using_rpc_mode = is_using_rpc_mode
        return self

    def set_broker_kind(self, broker_kind: int):
        self.boost_default_params.broker_kind = broker_kind
        return self


class RabbitmqDefaultConfig:
    """rabbitmq 默认配置"""
    RABBITMQ_USER = 'guest'
    RABBITMQ_PASSWORD = 'guest'
    RABBITMQ_HOST = '127.0.0.1'
    RABBITMQ_PORT = 5672
    RABBITMQ_VIRTUAL_HOST = '/'  # my_host 这个是rabbitmq 的虚拟子host用户自己创建的，如果你想直接用rabbitmq的根host 而不是使用虚拟子host,这里写 / 即可


class RabbitmqConfig(object):

    def __init__(self):          # noqa
        self.rabbitmq_default_config = RabbitmqDefaultConfig

    def set_rabbitmq_user(self, rabbitmq_user: str):
        self.rabbitmq_default_config.RABBITMQ_USER = rabbitmq_user
        return self

    def set_rabbitmq_password(self, rabbitmq_password: str):
        self.rabbitmq_default_config.RABBITMQ_PASSWORD = rabbitmq_password
        return self

    def set_rabbitmq_host(self, rabbitmq_host: str):
        self.rabbitmq_default_config.RABBITMQ_HOST = rabbitmq_host
        return self

    def set_rabbitmq_port(self, rabbitmq_port: int):
        self.rabbitmq_default_config.RABBITMQ_PORT = rabbitmq_port
        return self

    def set_rabbitmq_virtual_host(self, rabbitmq_virtual_host: str):
        self.rabbitmq_default_config.RABBITMQ_VIRTUAL_HOST = rabbitmq_virtual_host
        return self


class RedisDefaultConfig:
    """ Redis 默认配置"""
    REDIS_HOST = '127.0.0.1'
    REDIS_PASSWORD = ''
    REDIS_PORT = 6379
    REDIS_DB = 7  # redis消息队列所在db，请不要在这个db放太多其他键值对，框架里面有的功能会scan扫描键名
    REDIS_DB_FILTER_AND_RPC_RESULT = 8  # 如果函数做任务参数过滤 或者使用rpc获取结果，使用这个db，因为这个db的键值对多，和redis消息队列db分开


class RedisConfig(object):

    def __init__(self):               # noqa
        self.redis_default_config = RedisDefaultConfig

    def set_redis_host(self, redis_host: str):
        self.redis_default_config.REDIS_HOST = redis_host
        return self

    def set_redis_port(self, redis_port: int):
        self.redis_default_config.REDIS_PORT = redis_port
        return self

    def set_redis_password(self, redis_password: str):
        self.redis_default_config.REDIS_PASSWORD = redis_password
        return self

    def set_redis_db(self, redis_db: int):
        self.redis_default_config.REDIS_DB = redis_db
        return self

    def set_redis_filter_and_rpc_result(self, redis_filter_and_rpc_result: int):
        self.redis_default_config.REDIS_DB_FILTER_AND_RPC_RESULT = redis_filter_and_rpc_result
        return self
