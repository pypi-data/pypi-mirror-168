
import os
from threading import main_thread
from unittest.mock import MagicMock, patch, mock_open

from robojob import go

config = """
environment: test

path:
  - foo

parameters:
  param: value
"""


@patch('robojob.open', mock_open(read_data=config))
@patch('os.path.exists', MagicMock(return_value=True))
class TestGo:
    def test_environment_name(self):
        with go("test") as ctx:
            assert ctx.environment_name == "test"

    def test_param(self):
        with go("test") as ctx:
            assert ctx["param"] == "value"

    def test_add_path(self):
        path = os.environ["PATH"]
        with go("test") as ctx:
            ctx.add_path("foo")
            assert os.environ["PATH"].split(os.pathsep)[-1] == "foo"
        os.environ["PATH"] = path
        
    def test_path(self):
        path = os.environ["PATH"]
        with go("test", path="foo") as ctx:
            assert os.environ["PATH"].split(os.pathsep)[-1] == "foo"
        os.environ["PATH"] = path
        
        
