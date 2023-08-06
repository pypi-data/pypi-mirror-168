import amqpstorm
from amqpstorm.basic import Basic as AmqpStormBasic
from amqpstorm.queue import Queue as AmqpStormQueue
from deka_dubbo.publishers.base_publisher import AbstractPublisher
from deka_dubbo.dubbo_config import RabbitmqDefaultConfig
from deka_dubbo.publishers.base_publisher import deco_mq_conn_error


class RabbitmqPublisherUsingAmqpStorm(AbstractPublisher):
    # 使用amqpstorm 包实现的mq操作

    # noinspection PyAttributeOutsideInit
    def init_broker(self):
        self.logger.warning(f'使用AmqpStorm包 链接mq')
        self.connection = amqpstorm.UriConnection(
            f'amqp://{RabbitmqDefaultConfig.RABBITMQ_USER}:{RabbitmqDefaultConfig.RABBITMQ_PASSWORD}@'
            f'{RabbitmqDefaultConfig.RABBITMQ_HOST}:{RabbitmqDefaultConfig.RABBITMQ_PORT}/{RabbitmqDefaultConfig.RABBITMQ_VIRTUAL_HOST}?heartbeat={60 * 10}'
        )
        self.channel = self.connection.channel()   # type: amqpstorm.Channel
        self.channel_wrapper_by_amqpstormbasic = AmqpStormBasic(self.channel)
        self.queue = AmqpStormQueue(self.channel)
        self.queue.declare(queue=self.queue_name, durable=True)

    @deco_mq_conn_error
    def concrete_realization_publish(self, msg: str):
        self.channel_wrapper_by_amqpstormbasic.publish(exchange='',
                                                       routing_key=self.queue_name,
                                                       body=msg,
                                                       properties={'delivery_mode': 2}, )

    @deco_mq_conn_error
    def clear(self):
        self.queue.purge(self.queue_name)
        self.logger.warning(f'清除 {self.queue_name} 队列中的消息成功')

    @deco_mq_conn_error
    def get_message_count(self):
        return self.queue.declare(queue=self.queue_name, durable=True)['message_count']

    def close(self):
        self.channel.close()
        self.connection.close()
        self.logger.warning('关闭amqpstorm包 链接mq')
