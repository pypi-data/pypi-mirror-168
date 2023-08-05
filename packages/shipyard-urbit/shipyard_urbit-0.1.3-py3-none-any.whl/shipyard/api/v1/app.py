from fastapi import FastAPI
from multiprocessing import current_process
from shipyard.tasks import Task, TaskRunner

app = FastAPI()

@app.get("/")
async def root():
    print(current_process().pid)
    TaskRunner.run(Task(3))
    return {"message": "Hello Breh"}
