import logging
import os
import subprocess
import tempfile
import uuid

from .task_execution import TaskExecution, TaskException


_mandatory = (
    "source_server",
    "source_database",
    "source_schema",
    "source_table",
    "target_server",
)

class BcpExecution(TaskExecution):
    def __init__(self, name="", truncate_target=True):
        super().__init__(name=name)
        self.truncate_target = truncate_target

    def bind_parameters(self, context_parameters):
        self.parameters["tempfile"] = "".join((os.path.join(tempfile.gettempdir(), str(uuid.uuid4())), '.bcp'))
        self.parameters["logfile"] = "".join((self.parameters["tempfile"], '.log'))
        for mandatory_parameter in _mandatory:
            self.parameters[mandatory_parameter] = context_parameters[mandatory_parameter]
        self.parameters["odbc_driver"] = context_parameters.get("odbc_driver")
        self.parameters["target_database"] = context_parameters.get("target_database") or context_parameters["source_database"]
        self.parameters["target_schema"] = context_parameters.get("target_schema") or context_parameters["source_schema"]
        self.parameters["target_table"] = context_parameters.get("target_table") or context_parameters["source_table"]

    def execute(self):
        self.load_from_source()
        self.load_to_target()

    def load_from_source(self):
        source_table = f'[{self.parameters["source_database"]}].[{self.parameters["source_schema"]}].[{self.parameters["source_table"]}]'
        tempfile = self.parameters["tempfile"]
        options = [ "-T", "-n", "-S", self.parameters["source_server"] ]
        result = subprocess.run(["bcp.exe", source_table, "OUT", tempfile] + options, capture_output=True)
        if result.stderr:
            raise TaskException(result.stderr)

    def load_to_target(self):
        if self.truncate_target:
            self.truncate()
        target_table = f'[{self.parameters["target_database"]}].[{self.parameters["target_schema"]}].[{self.parameters["target_table"]}]'
        tempfile = self.parameters["tempfile"]
        logfile = self.parameters["logfile"]
        options = [ "-T", "-n", "-S", self.parameters["target_server"], "-h", "TABLOCK" ]
        try:
            result = subprocess.run(["bcp.exe", target_table, "IN", tempfile] + options, capture_output=True)
            with open(logfile, 'wb') as log:
                log.write(result.stderr)
                log.write(result.stdout)
        finally:
            os.remove(tempfile)
        if result.stderr:
            raise TaskException(result.stderr)

    def truncate(self):
        import pyodbc
        odbc_driver = self.parameters["odbc_driver"]
        target_server = self.parameters["target_server"]
        target_database = self.parameters["target_database"]
        target_schema = self.parameters["target_schema"]
        target_table = self.parameters["target_table"]

        connstr = f"Driver={odbc_driver};Server={target_server};Database={target_database};Trusted_Connection=yes;"
        conn = pyodbc.connect(connstr)
        conn.execute(f"TRUNCATE TABLE [{target_schema}].[{target_table}]")
        conn.commit()
        conn.close()


logging.basicConfig(level="DEBUG")
if __name__=="__main__":
    from .. import go
    with go("BCP") as ctx:
        for ctx["source_table"] in ctx["tables"]:
            ctx.process_task_execution(BcpExecution(name=ctx["source_table"]))
