import json

import amqpstorm

from deka_dubbo.consumers.base_consumer import AbstractConsumer
from deka_dubbo.publishers.rabbitmq_amqpstorm_publisher import RabbitmqPublisherUsingAmqpStorm


class RabbitmqConsumerAmqpStorm(AbstractConsumer):
    """
    使用AmqpStorm实现的，对线程安全的，不用加锁。
    """
    BROKER_KIND = 0

    def shedual_task(self):

        def callback(amqpstorm_message: amqpstorm.Message):
            body = amqpstorm_message.body
            self.print_message_get_from_broker('rabbitmq', body)
            body = json.loads(body)
            kw = {'amqpstorm_message': amqpstorm_message, 'body': body}
            self.submit_task(kw)

        rp = RabbitmqPublisherUsingAmqpStorm(self.queue_name, logger=self.logger)
        rp.init_broker()
        rp.channel_wrapper_by_amqpstormbasic.qos(self.concurrent_num)
        rp.channel_wrapper_by_amqpstormbasic.consume(callback=callback, queue=self.queue_name, no_ack=False)
        rp.channel.start_consuming(auto_decode=True)

    def confirm_consume(self, kw):
        try:
            kw['amqpstorm_message'].ack()  # 确认消费
        except Exception as e:
            self.logger.error(f'AmqpStorm确认消费失败  {type(e)} {e}')

    def requeue(self, kw):
        kw['amqpstorm_message'].nack(requeue=True)