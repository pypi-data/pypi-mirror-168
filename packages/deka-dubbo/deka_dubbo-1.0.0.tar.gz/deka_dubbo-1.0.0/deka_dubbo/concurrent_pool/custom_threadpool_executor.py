import os
import queue
import threading
import weakref
from concurrent.futures import Executor, Future
from deka_dubbo.utils.get_logger import get_default_logger, Logger

shutdown = False
thread_queues = weakref.WeakKeyDictionary()


class _WorkItem(object):
    def __init__(self, future, fn, args, kwargs):
        self.future = future
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.logger = Logger.logger

    def run(self):
        # noinspection PyBroadException
        if not self.future.set_running_or_notify_cancel():
            return
        try:
            result = self.fn(*self.args, **self.kwargs)
        except BaseException as exc:
            self.logger.exception(f'函数 {self.fn.__name__} 中发生错误，错误原因是 {type(exc)} {exc}')
            self.future.set_exception(exc)
            # Break a reference cycle with the exception 'exc'
            self = None      # noqa
        else:
            self.future.set_result(result)

    def __str__(self):
        return f'{(self.fn.__name__, self.args, self.kwargs)}'


class ThreadPoolExecutorShrinkAble(Executor):

    # 最小值可以设置为0，代表线程池无论多久没有任务最少要保持多少个线程待命
    MIN_WORKERS = 5
    # 当前线程从queue.get(block=True, timeout=KEEP_ALIVE_TIME)多久没任务，就线程结束
    KEEP_ALIVE_TIME = 60

    def __init__(self, max_workers: int = None, thread_name_prefix=''):
        """
        :param max_workers:  线程池最大线程数量
        :param thread_name_prefix:   线程名称前缀
        """
        self.max_workers = max_workers or (os.cpu_count() or 1) or 5
        self.thread_name_prefix = thread_name_prefix
        self.work_queue = queue.Queue(10)
        self.threads = weakref.WeakSet()
        self.lock_compute_threads_free_count = threading.Lock()
        self.threads_free_count = 0
        self._shutdown = False
        self._shutdown_lock = threading.Lock()
        self.pool_ident = id(self)

    def change_thread_free_count(self, change_num):
        with self.lock_compute_threads_free_count:
            self.threads_free_count += change_num

    def submit(self, func, *args, **kwargs):
        with self._shutdown_lock:
            if self._shutdown:
                raise RuntimeError('不能添加新的任务到线程池')
            f = Future()
            w = _WorkItem(f, func, args, kwargs)
            self.work_queue.put(w)
            self._adjust_thread_count()
            return f

    def _adjust_thread_count(self):
        if self.threads_free_count <= self.MIN_WORKERS and len(self.threads) < self.max_workers:
            t = _CustomThread(self)
            t.daemon = True
            t.start()
            self.threads.add(t)
            thread_queues[t] = self.work_queue

    def shutdown(self, wait=True):  # noqa
        with self._shutdown_lock:
            self._shutdown = True
            self.work_queue.put(None)
        if wait:
            for t in self.threads:
                t.join()


class _CustomThread(threading.Thread):
    lock_for_judge_threads_free_count = threading.Lock()

    def __init__(self, executorx: ThreadPoolExecutorShrinkAble):
        super().__init__()
        self.executorx = executorx
        self.logger = Logger.logger

    # noinspection PyUnresolvedReferences
    def remove_thread(self, stop_reason=''):
        # logger = Logger.logger
        self.logger.debug(f'停止线程 {self._ident}, 触发条件是 {stop_reason}')
        self.executorx.change_thread_free_count(-1)
        self.executorx.threads.remove(self)
        thread_queues.pop(self)

    # noinspection PyUnresolvedReferences
    def run(self):
        # logger = Logger.logger
        self.logger.debug(f'新启动线程 {self._ident}')
        self.executorx.change_thread_free_count(1)
        while True:
            try:
                work_item = self.executorx.work_queue.get(block=True, timeout=self.executorx.KEEP_ALIVE_TIME)
            except queue.Empty:
                with self.lock_for_judge_threads_free_count:
                    if self.executorx.threads_free_count > self.executorx.MIN_WORKERS:
                        self.remove_thread(
                            f'{self.executorx.pool_ident} 线程池中的 {self.ident} 线程超过 {self.executorx.KEEP_ALIVE_TIME}'
                            f'秒没有任务，线程池中不在工作状态中的线程数量是 {self.executorx.threads_free_count},'
                            f'超过了指定的最小核心数量 {self.executorx.MIN_WORKERS}')
                        break
                    else:
                        continue
            if work_item is not None:
                self.executorx.change_thread_free_count(-1)
                work_item.run()
                del work_item
                self.executorx.change_thread_free_count(1)
                continue
            if shutdown or self.executorx.shutdown:
                self.executorx.work_queue.put(None)
                break
