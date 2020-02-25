from src.jobs.config import huey

@huey.task()
def test_task():
    print("TEST TASK OMG")
