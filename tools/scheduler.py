import time
import threading
from typing import Callable, List


class Task:

    def __init__(self, priority: int, cycle_length: int, function: Callable, *args, **kwargs):
        self.priority = priority
        self.cycle_length = cycle_length
        self.function = function
        self.args = args
        self.kwargs = kwargs

    @classmethod
    def new(cls, priority: int, cycle_length: int, function: Callable, *args, **kwargs) -> 'Task':
        return cls(priority, cycle_length, function, *args, **kwargs)

    @property
    def run_when(self) -> int:
        return int(time.time()) + self.cycle_length


class Scheduler:
    """
    Please don't use me! I'm not finished yet!
    """

    def __init__(self):
        self.tasks: List[Task] = []
        raise NotImplementedError


    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def run_tasks(self) -> None:
        for task in self.tasks:
            if task.run_when <= time.time():
                task.function(*task.args, **task.kwargs)

    def loop(self):
        pass


