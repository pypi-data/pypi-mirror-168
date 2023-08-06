class ConcurrentModeEnum:
    THREADING = 1
    ASYNC = 2     # asyncio, 适用于async def定义的函数
    SINGLE_THREAD = 3


class BrokerEnum:
    # 使用amqpstorm 包操作rabbitmq 作为 分布式消息队列， 支持消费确认。
    RABBITMQ_AMQPSTORM = 0
    # 使用redis 的list 结构，brpop 作为分布式消息队列。随意重启和关闭将会丢失大量消息，不支持消费确认。
    # 注重性能不在乎丢失消息可选择这个redis 方案
    REDIS_STREAM = 1

