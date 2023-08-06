import asyncio
import atexit
import threading
import time
import traceback


class AsyncPoolExecutor(object):

    def __init__(self, size, loop=None):
        """
        :param size: 同时并发运行的协程任务数量
        :param loop:
        """
        self.size = size
        self.loop = loop or asyncio.new_event_loop()
        self.sem = asyncio.Semaphore(self.size, loop=self.loop)
        self.queue = asyncio.Queue(maxsize=size, loop=self.loop)
        self.lock = threading.Lock()
        t = threading.Thread(target=self.start_loop_in_new_thread)
        t.setDaemon(True)
        t.start()
        self.can_be_closed_flag = False
        atexit.register(self.shutdown)

        self.event = threading.Event()
        self.event.set()

    def submit(self, func, *args, **kwargs):
        future = asyncio.run_coroutine_threadsafe(self.produce(func, *args, **kwargs), self.loop)
        future.result()

    async def produce(self, func, *args, **kwargs):
        await self.queue.put((func, args, kwargs))

    async def consume(self):
        while True:
            func, args, kwargs = await self.queue.get()
            if isinstance(func, str) and func.startswith('stop'):
                break
            # noinspection PyBroadException,PyUnusedLocal
            try:
                await func(*args, **kwargs)
            except Exception as e:
                traceback.print_exc()

    async def __run(self):
        for _ in range(self.size):
            asyncio.ensure_future(self.consume())

    def start_loop_in_new_thread(self):
        self.loop.run_until_complete(asyncio.wait([self.consume() for _ in range(self.size)], loop=self.loop))
        self.can_be_closed_flag = True

    def shutdown(self):
        if self.loop.is_running():
            for i in range(self.size):
                self.submit(f'stop{i}', )
            while not self.can_be_closed_flag:
                time.sleep(0.1)
            self.loop.stop()
            self.loop.close()
            print('关闭循环')
