import json
import time
import typing
from collections import OrderedDict

from deka_dubbo.utils.redis_manager import RedisMixin
from deka_dubbo.utils import decorators
"""
任务消费完成后，如果重复发布则过滤，分别实现永久性过滤重复任务和过滤有效期内的重复任务
任务过滤 = 函数参数过滤 = 字典过滤 = 排序后的键值对json字符串过滤
"""


class RedisFilter(RedisMixin):
    """
    使用set结构
    基于函数参数的任务过滤。这个是永久性的过滤，除非自己手动删除这个键
    """
    def __init__(self, redis_key_name, redis_filter_task_expire_seconds):
        """
        :param redis_key_name: 任务过滤键
        :param redis_filter_task_expire_seconds: 任务过滤的过期时间
        """
        self.redis_key_name = redis_key_name
        self.redis_filter_task_expire_seconds = redis_filter_task_expire_seconds

    @staticmethod
    def get_ordered_str(value):
        """对json的键值对在redis 中进行过滤，需要先把键值对排序，否则过滤会不准确"""
        if isinstance(value, str):
            value = json.loads(value)
        ordered_dict = OrderedDict()
        for k in sorted(value):
            ordered_dict[k] = value[k]
        return json.dumps(ordered_dict)

    def add_a_value(self, value: typing.Union[str, dict]):
        self.redis_db_filter_and_rpc_result.sadd(self.redis_key_name, self.get_ordered_str(value))

    def check_value_exists(self, value):
        return self.redis_db_filter_and_rpc_result.sismember(self.redis_key_name, self.get_ordered_str(value))

    def delete_expire_filter_task_cycle(self, logger):
        pass


class RedisImpermanencyFilter(RedisFilter):
    """
    使用zset结构
    基于函数参数的任务过滤，这个是非永久性的过滤。
    """

    @decorators.keep_circulating(60, block=False)
    def delete_expire_filter_task_cycle(self, logger):
        """
        一直循环删除过期的过滤任务。任务过滤过期时间最好不要小于60秒，否则删除会不及时,导致发布的新任务不能触发执行。
        一般实时价格接口是缓存5分钟或30分钟
        :return:
        """
        time_max = time.time() - self.redis_filter_task_expire_seconds
        delete_num = self.redis_db_filter_and_rpc_result.zremrangebyscore(self.redis_key_name, 0, time_max)
        logger.warning(f'从 {self.redis_key_name} 键删除 {delete_num} 个过期的过滤任务')
        logger.warning(f'{self.redis_key_name} 键中有 {self.redis_db_filter_and_rpc_result.zcard(self.redis_key_name)} '
                       f'个没有过期的任务')

    def add_a_value(self, value: typing.Union[str, dict]):
        self.redis_db_filter_and_rpc_result.zadd(self.redis_key_name, self.get_ordered_str(value), time.time())

    def manual_delete_a_value(self, value: typing.Union[str, dict]):
        self.redis_db_filter_and_rpc_result.zrem(self.redis_key_name, self.get_ordered_str(value))

    def check_value_exists(self, value):
        return False if self.redis_db_filter_and_rpc_result.zrank(self.redis_key_name, self.get_ordered_str(value)) is None else True
