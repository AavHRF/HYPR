I figured the scheduler deserved a bit of documentation considering that the code behind it is somewhat cursed.
Fortunately, I wrote it, so I can write the documentation without taking 10d10 sanity damage.

Scheduler methods:
- `add_task(self, task: Task) -> None`
- `organize(self) -> None`
- `run(self) -> None`
  - `check_if_task_is_due(self, task: Task) -> bool`
  - `run_task(self, task: Task) -> None`

Basically, there are three methods that can be called in the scheduler class: `add_task`, `organize`, and `run`.

`add_task` is realistically the only method that should be called by external code at any point, beyond the initial
call to `run`. As it says on the tin, it takes a `Task` object, and adds it to the queue of the scheduler.

`organize` sorts the queue by when the next task needs to be run -- note: it does not sort by any form of priority.

`run` is where things get fun. It goes through the queue, and checks to see if there are tasks. If there aren't any tasks,
it waits for a task to be added with `threading.Signal()`. If there *are* tasks, it runs the first task in the queue, and
then does one of two things:
1. It finds a new task that has been added to the queue. If it does, it re-sorts the queue, checks to see if the task needs to be run, and if so, it runs it.
2. Oooor, it spawns a background thread to run the next task in the queue with a delay of however long until that task needs to run.

If there's nothing in the queue at all, it waits for a task to be added.