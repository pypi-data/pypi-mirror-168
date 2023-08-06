from unittest.mock import MagicMock

from robojob.job_execution import JobExecution
from robojob.task_execution import TaskExecution

class MockTaskExecution(TaskExecution):
    def __init__(self):
        super().__init__("mock")
        self.mock = MagicMock()

    def bind_parameters(self, context_parameters):
        self.value = context_parameters["param"]

    def execute(self):
        pass

def test_call_with_no_arguments():
    mock = MagicMock()
    def task():
        mock()

    with JobExecution() as ctx:
        ctx.execute(task)
    
    mock.assert_called_once()

def test_call_with_constructor_arguments():
    mock = MagicMock()
    def task(param):
        mock(param)

    with JobExecution(parameters={"param": "value"}) as ctx:
        ctx.execute(task)

    mock.assert_called_once_with("value")

def test_call_with_local_arg():
    mock = MagicMock()
    def task(param):
        mock(param)

    with JobExecution() as ctx:
        ctx["param"] = "value"
        ctx.execute(task)

    mock.assert_called_once_with("value")
