import pytest
from unittest.mock import MagicMock

from robojob.job_execution import JobException, JobExecution
from robojob.task_execution import TaskExecution


class MyTestException(Exception):
    pass


def fail():
    raise MyTestException()


def test_backend_called():
    "The backend gets called on entry and exit"
    ctx = JobExecution(backend=MagicMock())

    with ctx:
        pass

    ctx.backend.before_job_execution.assert_called_once()
    ctx.backend.after_job_execution.assert_called_once()
    assert ctx.status == "Completed"

def test_backend_called_with_task():
    "The backend gets called on entry and exit"
    ctx = JobExecution(backend=MagicMock())
    
    def task(): pass
    
    with ctx:
        ctx.execute(task)

    ctx.backend.before_job_execution.assert_called_once()
    ctx.backend.after_job_execution.assert_called_once()
    ctx.backend.before_task_execution.assert_called_once()
    ctx.backend.after_task_execution.assert_called_once()
    assert ctx.status == "Completed"


def test_backend_called_on_task_failure():
    "The backend gets called on entry and exit, even if a task fails"
    ctx = JobExecution(backend=MagicMock())
    try:
        with ctx:
            ctx.execute(fail)
    except:
        pass

    ctx.backend.before_job_execution.assert_called_once()
    ctx.backend.after_job_execution.assert_called_once()
    assert ctx.status == "Failed"


def test_backend_called_on_job_failure():
    "The backend gets called on entry and exit, even if a task fails"
    ctx = JobExecution(backend=MagicMock())
    try:
        with ctx:
            x = 1/0
    except:
        pass

    ctx.backend.before_job_execution.assert_called_once()
    ctx.backend.after_job_execution.assert_called_once()
    assert ctx.status == "Failed"


def test_exception_reraised():
    "An exception raised by a task must be reraised when the the execution context is left"
    with pytest.raises(MyTestException):
        with JobExecution() as ctx:
            ctx.execute(fail)


def test_failure_stop_execution():
    "A failed task execution stops job execution."
    try:
        with JobExecution() as ctx:
            ctx.execute(fail)
            pytest.fail()
    except:
        pass

def test_early_exit():
    "Calling the exit() method ends job execution with no exceptions thrown"
    ctx = JobExecution()
    with ctx:
        ctx.exit()
        pytest.fail()
    assert ctx.status == "Completed"

def test_early_exit_with_custom_status():
    "Calling the exit() method ends job execution with no exceptions thrown"
    ctx = JobExecution()
    with ctx:
        ctx.exit("Skipped")
        pytest.fail()
    assert ctx.status == "Skipped"

def test_on_error():
    on_error = MagicMock()
    try:
        with JobExecution() as ctx:
            ctx.on_error = on_error
            ctx.execute(fail)
    except:
        pass
            
    on_error.bind_parameters.assert_called_once()
    on_error.execute_with_logging.assert_called_once()
