import logging

from .version import __version__

class SqlServerBackend:
    def __init__(self, connection):
        self.connection = connection

    def before_job_execution(self, job_execution):
        cursor = self.connection.execute(_JOB_EXECUTION_INSERT,
                                         job_execution.id,
                                         job_execution.environment_name,
                                         job_execution.job_name,
                                         job_execution.status,
                                         __version__
                                         )
        ((job_execution_id,),) = cursor.execute("SELECT @@IDENTITY AS JobExecutionID")
        logging.info(f"Job execution id = {job_execution_id}")
        job_execution["job_execution_id"] = job_execution_id

    def before_task_execution(self, task_execution):
        cursor = self.connection.execute(_TASK_EXECUTION_INSERT,
                                         task_execution.id,
                                         task_execution.job_execution.id,
                                         task_execution.__class__.__name__,
                                         task_execution.name,
                                         task_execution.status,
                                         )
        
        for name, value in sorted(task_execution.parameters.items()):
            if name.lower().endswith("password"):
                value = "[secret]"
            cursor.execute("INSERT INTO dbo.TaskExecutionParameter (TaskExecutionGUID, ParameterName, ParameterValue) VALUES (?, ?, ?);",
                            task_execution.id,
                            name,
                            str(value))

    def after_task_execution(self, task_execution):
        self.connection.execute(_TASK_EXECUTION_UPDATE,
                                task_execution.status,
                                task_execution.error_message,
                                task_execution.id)

    def after_job_execution(self, job_execution):
        self.connection.execute(_JOB_EXECUTION_UPDATE,
                                job_execution.status,
                                job_execution.error_message,
                                job_execution.id)


_JOB_EXECUTION_INSERT = """
INSERT INTO dbo.JobExecution (
    JobExecutionGUID
  , EnvironmentName
  , JobName
  , StartedOn
  , Status
  , RobojobVersion
  )
VALUES (
    ? -- JobExecutionGUID
  , ? -- EnvironmentName
  , ? -- JobName
  , SYSUTCDATETIME() -- StartedOn
  , ? -- Status
  , ?
  );
"""

_JOB_EXECUTION_UPDATE = """
UPDATE dbo.JobExecution
SET CompletedOn = SYSUTCDATETIME()
  , Status = ?
  , ErrorMessage = ?
WHERE JobExecutionGUID = ?;
"""

_TASK_EXECUTION_INSERT = """
INSERT INTO dbo.TaskExecution (
    TaskExecutionGUID
  , JobExecutionGUID
  , TaskTypeName
  , TaskName
  , StartedOn
  , Status
  )
VALUES (
    ? -- JobExecutionGUID
  , ? -- TaskExecutionGUID
  , ? -- TaskTypeName
  , ? -- TaskName
  , SYSUTCDATETIME() -- StartedOn
  , ? -- Status
)
"""

_TASK_EXECUTION_UPDATE = """
UPDATE dbo.TaskExecution
SET CompletedOn = SYSUTCDATETIME()
  , Status = ?
  , ErrorMessage = ?
WHERE TaskExecutionGUID = ?;
"""

