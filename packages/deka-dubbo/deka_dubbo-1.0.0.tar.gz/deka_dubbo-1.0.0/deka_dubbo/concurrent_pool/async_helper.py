import asyncio
from concurrent.futures import Executor
from functools import partial

from deka_dubbo.concurrent_pool.custom_threadpool_executor import ThreadPoolExecutorShrinkAble

async_executor_default = ThreadPoolExecutorShrinkAble()


async def simple_run_in_executor(f, *args, async_executor: Executor = None, async_loop=None, **kwargs):
    """
    :param f:  f是一个同步的阻塞函数，f前面不能是由async定义的。
    :param args: f 函数的位置方式入参
    :param async_executor: 线程池
    :param async_loop: async的loop对象
    :param kwargs: f函数的关键字方式入参
    :return:
    """
    loopx = async_loop or asyncio.get_event_loop()
    async_executor = async_executor or async_executor_default
    result = await loopx.run_in_executor(async_executor, partial(f, *args, **kwargs))
    return result
