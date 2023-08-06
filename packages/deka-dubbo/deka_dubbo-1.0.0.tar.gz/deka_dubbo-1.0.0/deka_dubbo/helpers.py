from multiprocessing import Process
from typing import List
from deka_plog.log_manager import logger
# from deka_dubbo.factories.consumer_factory import get_consumer
# from deka_dubbo.consumers.base_consumer import ConsumersManager
from deka_dubbo.utils.get_logger import get_default_logger, Logger

class FunctionResultStatusPersistanceConfig(object):
    def __init__(self, is_save_status: bool, is_save_result: bool,
                 expire_seconds: int = 7 * 24 * 3600,
                 is_use_bulk_insert=False):
        """
        :param is_save_status: 是否保存状态
        :param is_save_result: 是否保存结果
        :param expire_seconds: 设置统计的过期时间
        :param is_use_bulk_insert: 是否使用批量插入来保存结果，
        批量插入是每隔0.5秒钟保存一次最近0.5秒内所有的函数消费状态结果
        """
        if not is_save_status and is_save_result:
            raise ValueError(f'你设置的是不保存函数运行状态, 但保存函数运行结果, 不允许这样设置!')
        self.is_save_status = is_save_status
        self.is_save_result = is_save_result
        # 如果设置的过期时间大于10天
        if expire_seconds > 10 * 24 * 3600:
            logger.warning('设置的时间过长，不能大于10天!')


def run_many_consumer_by_init_params(consumer_init_params_list: List[dict]):
    from deka_dubbo import get_consumer, ConsumersManager
    for consumer_init_params in consumer_init_params_list:
        get_consumer(**consumer_init_params).start_consumer_message()
    ConsumersManager.join_all_consumer_schedual_task_thread()


def run_consumer_with_multi_process(task_fun, process_num=1):
    """
    :param task_fun: 被装饰器装饰的消费函数
    :param process_num: 开启多个进程。 主要是 多进程并发 + 2中细粒度并发(threading, asyncio)。 叠加并发
    :return:
    """
    if not hasattr(task_fun, 'is_decorated_as_consume_function'):
        raise ValueError(f'{task_fun} 参数必须是一个被 boost 装饰的函数')
    if process_num == 1:
        task_fun.consume()
    else:
        for i in range(process_num):
            Process(target=run_many_consumer_by_init_params,
                    args=([{**{'consuming_function': task_fun}, **task_fun.init_params}],)).start()
