import time
import threading
from typing import Callable, List, Literal


class Task:
    def __init__(
        self,
        priority: Literal[1, 2, 3, 4, 5],
        tasktype: str,
        cycle_length: int,
        function: Callable,
        *args,
        **kwargs
    ):
        self.priority = priority
        self.cycle_length = cycle_length
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.type = tasktype
        self.init_time = int(time.time())

    @classmethod
    def new(
        cls,
        priority: Literal[1, 2, 3, 4, 5],
        tasktype: str,
        cycle_length: int,
        function: Callable,
        *args,
        **kwargs
    ) -> "Task":
        if priority not in [1, 2, 3, 4, 5]:
            raise ValueError("Priority must be between 1 and 5")
        return cls(priority, tasktype, cycle_length, function, *args, **kwargs)

    @property
    def run_when(self) -> int:
        return self.init_time + self.cycle_length


class Scheduler:
    def __init__(self):
        self.tasks: List[Task] = []
        self.organize()
        self.new_task_added = threading.Event()
        self.continue_running = False

    def add_task(self, task: Task) -> None:
        """
        Adds a task to the scheduler, reorganizes the tasks, and notifies the scheduler of a new task.
        :param task: Task
        :return: None
        """
        self.tasks.append(task)
        self.organize()
        self.new_task_added.set()

    def organize(self) -> None:
        """
        Method to organize the tasks by time of execution, placing higher priority tasks first.
        :return:
        """
        self.tasks.sort(key=lambda task: task.run_when)
        previous_task: Task = self.tasks[0]
        for task in self.tasks[1:]:
            if task.run_when == previous_task.run_when:
                if task.priority < previous_task.priority:
                    # Swap the tasks
                    self.tasks[self.tasks.index(task)] = previous_task
                    self.tasks[self.tasks.index(previous_task)] = task
                    previous_task = task
                else:
                    self.tasks.remove(task)
                    self.tasks.insert(0, task)
                    previous_task = task
        return

    def run(self) -> None:
        """
        This method is the main loop of the scheduler. It should be called once to start the scheduler, and never again.
        If you value your sanity, you will not look through this code.
        :return:
        """

        # Threading locks to make sure that only one task is contacting NationStates at any given time.
        global_api_lock = threading.Lock()
        global_recruitment_lock = threading.Lock()
        global_telegram_lock = threading.Lock()

        def check_if_task_is_due(task: Task) -> bool:
            return task.run_when <= int(time.time())

        def run_task(task: Task, delay: int = 0) -> None:

            if delay > 0:
                time.sleep(delay)

            global_api_lock.acquire()
            if task.type == "recruitment":
                with global_telegram_lock:
                    with global_recruitment_lock:
                        try:
                            task.function(*task.args, **task.kwargs)
                        except Exception as e:
                            print(e)
                            global_api_lock.release()
                        global_api_lock.release()
                        time.sleep(task.cycle_length)
            elif task.type == "telegram":
                with global_telegram_lock:
                    try:
                        task.function(*task.args, **task.kwargs)
                    except Exception as e:
                        print(e)
                        global_api_lock.release()
                    global_api_lock.release()
                    time.sleep(task.cycle_length)
            else:
                task.function(*task.args, **task.kwargs)
                time.sleep(task.cycle_length)
            return

        while self.continue_running:
            # Check if there are any tasks to run
            if self.tasks:
                # Check if the first task is due
                if check_if_task_is_due(self.tasks[0]):
                    # Run the task and then clean up the queue
                    run_task(self.tasks[0])
                    self.tasks.pop(0)
                    self.organize()

                # Check to see if there are any new tasks
                if self.new_task_added.is_set():
                    # There's a new task in the queue. Clear the flag so that we don't get stuck in a loop,
                    # and then reorganize the queue and check when the first task is due to be run.
                    self.new_task_added.clear()
                    self.organize()
                    if check_if_task_is_due(self.tasks[0]):
                        t = threading.Thread(target=run_task, args=(self.tasks[0], 0))
                        t.start()
                else:
                    # Spawn a background thread to run the task, and then wait for the next task to be due
                    t = threading.Thread(
                        target=run_task,
                        args=(self.tasks[0], self.tasks[0].run_when - int(time.time())),
                    )
                    t.start()
                    # Remove the task that we just ran from the queue
                    self.tasks.pop(0)
                    if len(self.tasks) > 1:
                        self.organize()
                    else:
                        # There is nothing in the queue, so wait for a task to be added
                        self.new_task_added.wait()
            else:
                # If there are no tasks, wait for a new task to be added
                self.new_task_added.wait()
        return
