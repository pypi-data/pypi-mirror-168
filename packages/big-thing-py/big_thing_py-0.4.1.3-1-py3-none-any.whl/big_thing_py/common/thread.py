from big_thing_py.utils import *
from big_thing_py.common import *
from typing import *

from threading import Thread, Event, Lock
from queue import Queue


class SoPThread:
    def __init__(self, name: str = None, func: Callable = None, arg_list: Tuple = (), kwargs_list: dict = {}, daemon: bool = True, mode: List[str] = []) -> None:
        self._name: str = name
        self._func: Callable = func
        self._arg_list: Tuple = arg_list
        self._kwargs_list: dict = kwargs_list
        self._daemon: List[str] = daemon
        self._mode: List[str] = mode

        self._thread = Thread()
        self._exit_event = Event()
        self._lock = Lock()

        if func:
            self.set_thread()
        else:
            SOPLOG_DEBUG('[THREAD] No function to run', 'red')
            raise Exception()

    def set_thread(self) -> None:
        self._arg_list: list = list(self._arg_list)

        if type(self._mode) == str:
            self._mode = [self._mode]

        if 'lock' in self._mode:
            self._arg_list.insert(0, self._lock)
        if 'event' in self._mode:
            self._arg_list.insert(0, self._exit_event)
        else:
            for mode in self._mode:
                if mode not in ['event', 'lock']:
                    raise Exception(f'unknown SoPThread mode: {mode}')

        self._arg_list = tuple(self._arg_list)

        if not self._name:
            self._name = '_'.join(self._func.__name__.split('_')[:-1])

        self._thread = Thread(
            target=self._func, name=self._name, daemon=self._daemon, args=self._arg_list, kwargs=self._kwargs_list)

    def start(self) -> None:
        self._thread.start()

    def join(self) -> None:
        self._thread.join()

    def exit(self) -> None:
        self._exit_event.set()

    def is_exit(self) -> bool:
        return self._exit_event.is_set()

    def get_name(self) -> str:
        return self._name
