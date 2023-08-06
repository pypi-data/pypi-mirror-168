import copy
from typing import Callable

from deka_dubbo.utils.get_logger import get_default_logger
from deka_dubbo.publishers.rabbitmq_amqpstorm_publisher import RabbitmqPublisherUsingAmqpStorm

broker_kind_publisher_type_map = {
    0: RabbitmqPublisherUsingAmqpStorm,
    # 1: RedisStreamPublisher,
}


def get_publisher(queue_name, *, logger=get_default_logger(), log_level_int=10, log_prefix='', log_write_to_file=False,
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
    all_kwargs = copy.copy(locals())
    all_kwargs.pop('broker_kind')
    if broker_kind not in broker_kind_publisher_type_map:
        raise ValueError(f'设置的中间件种类数字不正确,你设置的值是 {broker_kind}')
    return broker_kind_publisher_type_map[broker_kind](**all_kwargs)

