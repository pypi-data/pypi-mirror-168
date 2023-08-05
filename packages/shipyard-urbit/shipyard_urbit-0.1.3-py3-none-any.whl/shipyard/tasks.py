from multiprocessing import current_process, get_context
from multiprocessing.connection import Client, Listener


class Task:
    def __init__(self, id: int):
        self.id = id

    def run(self):
        print(f"Taskin {self.id}: {current_process().pid}")


class TaskRunner:
    def __init__(self):
        self.process = get_context("spawn").Process(target=self.start_listener)

    def __enter__(self):
        print("Starting TaskRunner")
        self.process.start()
        return self

    def __exit__(self, type, value, traceback):
        self.process.terminate()
        self.process.join()

    def start_listener(self):
        try:
            with Listener(("127.0.0.1", 57778)) as listener:
                while True:
                    with listener.accept() as conn:
                        task = conn.recv()
                        if isinstance(task, Task):
                            task.run()
        except (KeyboardInterrupt, SystemExit):
            print()
            print("Shutting down TaskRunner")

    @classmethod
    def run(cls, task: Task):
        with Client(("127.0.0.1", 57778)) as conn:
            conn.send(task)
