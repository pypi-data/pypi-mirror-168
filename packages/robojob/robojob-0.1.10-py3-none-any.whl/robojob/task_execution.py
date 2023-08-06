
import datetime
import logging
import uuid


class TaskException(Exception):
    pass

class TaskExecution:
    def __init__(self, name):
        self.name = name
        self.job_execution = None
        self.parameters = dict()
        self.id = uuid.uuid4()
        self.status = ""
        self.started_at = None
        self.completed_at = None
        self.running_time = None
        self.error_message = ""

    def bind_parameters(self, context_parameters):
        raise NotImplementedError()

    def execute_with_logging(self):
        logging.info(f"Task starting: {self}")
        self.status = "Started"
        for key, value in self.parameters.items():
            logging.debug(f"Parameter: {key} = {repr(value)}")
        self.started_at = datetime.datetime.utcnow()
        try:
            self.execute()
            self.status = "Completed"
        except Exception as e:
            self.status = "Failed"
            self.error_message = str(e)
            logging.error(f"Task failed: {self.error_message}")
            raise
        finally:
            self.completed_at = datetime.datetime.utcnow()
            self.running_time = self.completed_at - self.started_at
            logging.info(f"Task completed with status {self.status}")
            logging.info(f"Running time: {self.running_time}")

    def execute(self):
        raise NotImplementedError()

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.id} ({self.name})>"

