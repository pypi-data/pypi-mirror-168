import datetime
import logging
import os
import socket
import uuid
import traceback
from typing import Any, Dict


from .parameter_collection import ParameterCollection
from .function import FunctionExecution
from .powershell import PowershellExecution
from .r import RExecution
from .sql import StoredProcedureExecution
from .email import EmailExecution
from .task_execution import TaskExecution

class JobException(Exception): pass

class UserExitException(JobException):
    def __init__(self, status):
        self.status = status

class JobExecution:
    """
    Context manager for logging job executions.
    """
    def __init__(self, job_name=None,
                       environment_name=None,
                       backend=None,
                       path=None,
                       parameters=None
                       ):
        self.id = uuid.uuid4()
        self.job_name = job_name or "Anonymous job"
        self.backend = backend
        self.on_error = None
        self.parameters = ParameterCollection()
        self.environment_name = environment_name or socket.gethostname()
        self.status = ""
        self.error_message = ""
        if parameters:
            for key, value in parameters.items():
                self[key] = value
        if path:
            if isinstance(path, str):
                self.add_path(path)
            else:
                for path_element in path:
                    self.add_path(path_element)

    def __repr__(self):
        return f"<JobExecution: {self.id}>"

    def __enter__(self):
        logging.info(f"Job starting: {self}")
        self.status = "Started"
        self.started_at = datetime.datetime.utcnow()
        if self.backend:
            self.backend.before_job_execution(self)
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        suppress_exception = None
        self.completed_at = datetime.datetime.utcnow()
        self.running_time = self.completed_at - self.started_at
        if exc_value:
            if exc_type == UserExitException:
                self.status = exc_value.status
                suppress_exception = True
            else:
                self.status = "Failed"
                self.error_message = str(exc_value) + "\n" + "".join(traceback.format_tb(exc_tb))
                logging.error(f"Job failed: {exc_value}")
                if self.on_error:
                    logging.info(f"Invoking error handler")
                    try:
                        self.process_task_execution(self.on_error)
                    except:
                        logging.warning(f"Suppressing exception from task execution {self.on_error.id}")
        else:
            self.status = "Completed"
        logging.info(f"Job completed with status {self.status}")
        logging.info(f"Running time: {self.running_time}")
        if self.backend:
            self.backend.after_job_execution(self) 
        return suppress_exception

    def __setitem__(self, key, value):
        logging.debug(f"Setting parameter {key} = {repr(value)}")
        self.parameters[key] = value

    def __getitem__(self, key):
        params = self.get_parameters()
        return params[key]

    def get(self, key, default=None):
        return self.parameters.get(key, default)

    def __contains__(self, key):
        return key in self.parameters

    def add_path(self, path):
        logging.debug(f"Adding element to PATH: {path}")
        if not os.environ["PATH"].endswith(os.pathsep):
            os.environ["PATH"] += os.pathsep
        os.environ["PATH"] += path

    def export(self, variable_name):
        logging.debug(f"Exporting {variable_name}")
        value = self[variable_name]
    
        if isinstance(value, str):
            string_value = value
        elif isinstance(value, int):
            string_value = str(value)
        else:
            ValueError(f"Cannot export value {variable_name} (value is {repr(value)})")
        os.environ[variable_name.upper()] = string_value

    def exit(self, status="Completed"):
        raise UserExitException(status)

    def process_task_execution(self, task_execution : TaskExecution, local_parameters : Dict = {}):
        "Process a task execution in the context of the job execution."
        task_execution.job_execution = self
        task_execution.bind_parameters(self.get_parameters(local_parameters))
        if self.backend:
            self.backend.before_task_execution(task_execution)
        try:
            task_execution.execute_with_logging()
        finally:
            if self.backend:
                self.backend.after_task_execution(task_execution)
    

    def get_parameters(self, local_parameters : Dict = {}):
        parameters = self.parameters.copy()
        parameters.update(local_parameters)
        parameters["job_execution_guid"] = self.id
        parameters["job_name"] = self.job_name
        parameters["environment_name"] = self.environment_name
        parameters["status"] = self.status
        parameters["error_message"] = self.error_message
        return parameters

    def add_error_handler(self, error_handler):
        self.on_error = FunctionExecution(error_handler)

    def add_error_email(self, sender, recipients, subject, content, recipients_cc=[],):
        self.on_error = EmailExecution(sender=sender,
                                      recipients=recipients,
                                      subject=subject,
                                      content=content,
                                      recipients_cc=recipients_cc)
                                      
    def execute(self, function, **local_parameters):
        "Execute a function in the context of the job"
        self.process_task_execution(FunctionExecution(function), local_parameters)

    def execute_procedure(self, connection, schema_name, *procedure_names, **local_parameters):
        "Execute a stored procedure in the context of the job"
        if not procedure_names:
            raise JobException("At least one procedure name must be provided")
        for procedure_name in procedure_names:
            self.process_task_execution(StoredProcedureExecution(connection, schema_name, procedure_name), local_parameters)

    def execute_r(self, *script_names, **local_parameters):
        "Execute an R script in the context of the job"
        for script_name in script_names:
            self.process_task_execution(RExecution(script_name), local_parameters)

    def execute_powershell(self, *script_names, **local_parameters):
        "Execute a powershell script in the context of the job"
        for script_name in script_names:
            self.process_task_execution(PowershellExecution(script_name), local_parameters)

    def send_email(self,
                   sender,
                   recipients,
                   subject,
                   content,
                   recipients_cc=[],):
        "Send an email in the context of the job"
        self.process_task_execution(EmailExecution(sender=sender,
                                                  recipients=recipients,
                                                  subject=subject,
                                                  content=content,
                                                  recipients_cc=recipients_cc),
                                                  )
