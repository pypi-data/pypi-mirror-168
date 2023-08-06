from deka_dubbo.consumers.rabbitmq_amqpstorm_consumer import RabbitmqConsumerAmqpStorm

broker_kind_consumer_type_map = {
    0: RabbitmqConsumerAmqpStorm,
    # 1: RedisStreamConsumer,
}


def get_consumer(*args, broker_kind: int = None, **kwargs):
    """
    :param args: 入参是AbstractConsumer的入参
    :param broker_kind: 中间件种类
    :param kwargs:
    :return:
    """
    if broker_kind not in broker_kind_consumer_type_map:
        raise ValueError(f'设置的中间件种类数字不正确，你设置的值是{bool}')

    return broker_kind_consumer_type_map[broker_kind](*args, **kwargs)

