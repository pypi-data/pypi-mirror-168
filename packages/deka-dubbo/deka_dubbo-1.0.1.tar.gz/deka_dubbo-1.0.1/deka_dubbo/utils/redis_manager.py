import redis2 as redis
import redis3
# from deka_dubbo.utils.get_logger import glob_logger
from deka_dubbo.dubbo_config import RedisDefaultConfig
from deka_dubbo.utils.decorators import cached_method_result


class RedisManager(object):
    pool_dict = {}

    def __init__(self, host='127.0.0.1', port=6379, db=0, password=''):
        if (host, port, db, password) not in self.__class__.pool_dict:
            self.__class__.pool_dict[(host, port, db, password)] = redis.ConnectionPool(host=host, port=port,
                                                                                        db=db, password=password)
            self._r = redis.Redis(connection_pool=self.pool_dict[(host, port, db, password)])
            self._ping()

    def get_redis(self):
        """
        :return: redis.Redis
        """
        return self._r

    def _ping(self):
        try:
            self._r.ping()
        except Exception as e:
            raise e


class RedisMixin(object):
    """
    可以作为万能mixin被继承，也可以单独实例化使用
    """
    @property
    @cached_method_result
    def redis_db0(self):
        return RedisManager(host=RedisDefaultConfig.REDIS_HOST, port=RedisDefaultConfig.REDIS_PORT,
                            db=0, password=RedisDefaultConfig.REDIS_PASSWORD).get_redis()

    @property
    @cached_method_result
    def redis_db8(self):
        return RedisManager(host=RedisDefaultConfig.REDIS_HOST, port=RedisDefaultConfig.REDIS_PORT,
                            db=8, password=RedisDefaultConfig.REDIS_PASSWORD).get_redis()

    @property
    @cached_method_result
    def redis_db7(self):
        return RedisManager(host=RedisDefaultConfig.REDIS_HOST, port=RedisDefaultConfig.REDIS_PORT,
                            db=7, password=RedisDefaultConfig.REDIS_PASSWORD).get_redis()

    @property
    @cached_method_result
    def redis_db6(self):
        return RedisManager(host=RedisDefaultConfig.REDIS_HOST, port=RedisDefaultConfig.REDIS_PORT,
                            db=6, password=RedisDefaultConfig.REDIS_PASSWORD).get_redis()

    @property
    @cached_method_result
    def redis_db_frame(self):
        return RedisManager(host=RedisDefaultConfig.REDIS_HOST, port=RedisDefaultConfig.REDIS_PORT,
                            db=RedisDefaultConfig.REDIS_DB, password=RedisDefaultConfig.REDIS_PASSWORD).get_redis()

    @property
    @cached_method_result
    def redis_db_frame_version3(self):
        """redis3 和 redis2 入参差别很大，都要使用"""
        return redis3.Redis(host=RedisDefaultConfig.REDIS_HOST, port=RedisDefaultConfig.REDIS_PORT,
                            password=RedisDefaultConfig.REDIS_PASSWORD,
                            db=RedisDefaultConfig.REDIS_DB, decode_responses=True)

    @property
    @cached_method_result
    def redis_db_filter_and_rpc_result(self):
        return RedisManager(host=RedisDefaultConfig.REDIS_HOST, port=RedisDefaultConfig.REDIS_PORT,
                            db=RedisDefaultConfig.REDIS_DB_FILTER_AND_RPC_RESULT,
                            password=RedisDefaultConfig.REDIS_PASSWORD).get_redis()

    @property
    @cached_method_result
    def redis_db_filter_and_rpc_result_version3(self):
        return redis3.Redis(host=RedisDefaultConfig.REDIS_HOST, port=RedisDefaultConfig.REDIS_PORT,
                            db=RedisDefaultConfig.REDIS_DB_FILTER_AND_RPC_RESULT,
                            password=RedisDefaultConfig.REDIS_PASSWORD, decode_responses=True)

    def timestamp(self):
        """
        如果是多台机器做分布式控频 乃至确认消费, 每台机器取自己的时间,如果各机器的时间戳不一致会发生问题,
        改成统一使用从redis服务端获取时间
        """
        time_tuple = self.redis_db_frame_version3.time()
        return time_tuple[0] + time_tuple[1] / 1000000
