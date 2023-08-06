from unittest.mock import MagicMock

import pytest

from robojob.job_execution import JobExecution

def test_parameter_get_with_brackets():
    with JobExecution(parameters={"param": "value"}) as ctx:
        assert ctx["param"] == "value"

def test_parameter_set_with_brackets():
    with JobExecution() as ctx:
        ctx["param"] = "value"
        assert ctx["param"] == "value"

def test_parameter_get_method():
    with JobExecution() as ctx:
        ctx["param"] = "value"
        assert ctx.get("param") == "value"

def test_parameter_get_method_no_default():
    with JobExecution() as ctx:
        assert ctx.get("param") is None

def test_parameter_get_method_with_default():
    with JobExecution() as ctx:
        default = object()
        assert ctx.get("param", default) is default

def test_parameter_nonexistence_check():
    with JobExecution() as ctx:
        assert "param" not in ctx

def test_parameter_existence_check():
    with JobExecution() as ctx:
        ctx["param"] = "value"
        assert "param" in ctx


def test_fuzzy_name_matching():
    with JobExecution() as ctx:
        ctx["param"] = "value"
        assert ctx["@PARAM"] == "value"

def test_fuzzy_name_matching():
    with JobExecution() as ctx:
        ctx["param"] = "value"
        assert ctx["P_A_R_A_M"] == "value"

def test_fuzzy_binding_functions():
    mock = MagicMock()

    def fuzzy(pArAm):
        mock(pArAm)

    with JobExecution() as ctx:
        ctx["param"] = "value"
        ctx.execute(fuzzy)
    
    mock.assert_called_once_with("value")
    

def test_override():
    "Certain parameters values are hidden by built-in values"
    with JobExecution(job_name="job") as ctx:
        ctx["job_name"] = "something else"
        assert ctx["job_name"] == "job"

def test_undefined_parameter():
    def task(does_not_exist):
        pass

    with pytest.raises(KeyError):
        with JobExecution() as ctx:
            ctx.execute(task)

