import os
import pytest
from unittest.mock import MagicMock

from robojob.job_execution import JobException, JobExecution


def test_exported_value_visible_from_task():
    with JobExecution() as ctx:
        ctx["param"] = "value"
        ctx.export("param")

        def read_from_env():
            assert os.environ["param"] == "value"

        ctx.execute(read_from_env)

def test_export_fails_if_parameter_undefined():
    "Exporting an undefined parameter raises a KeyError"
    with pytest.raises(KeyError):
        with JobExecution() as ctx:
            ctx.export("does_not_exist")

def test_export_string():
    with JobExecution() as ctx:
        ctx["string"] = "value"
        ctx.export("string")
        assert os.environ["string"] == "value"

def test_export_integer():
    with JobExecution() as ctx:
        ctx["integer"] = 42
        ctx.export("integer")
        assert os.environ["integer"] == "42"

