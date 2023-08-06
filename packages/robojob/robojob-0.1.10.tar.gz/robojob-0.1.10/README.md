[[_TOC_]]

# Features

- *Job definition as code:* Jobs are Python code wrapped in a context manager.
- *Job configuration as data:* Parameter values and other configuration details can be stored in a configuration file, making it easy to deploy robojob jobs in different environments.
- *Dynamic parameter binding:* Parameter values are automatically bound to tasks at runtime, making job definitions easier to read. If a parameter is added to a task (e.g. a stored procedure), robojob will supply it to the task with no change to the job definition code.
- *Logging*: Parameter values used and errors raised by tasks are logged, and so are error thrown by the orchestration part of the job.

# API

## Code

The primary entry-point is the `go()` function which takes the following parameters:

- `job_name`: The name of the job.
- `config_path` (optional): The path of the configuration file. If this is not supplied, robojob will look for `robojob.yml`.
- `environment_name` (optional): The name of the environment.
- `backend` (optional): A Backend (TODO: Link to a section on backends).
- `path` (optional): One or more strings that will be appended to the PATH environment variable.
- `parameters` (optional): Job parameters (*Note: parameters with names that collide with those of built-in parameters will be ignored).

The `go()` function returns a `JobExecution()` that can be used as a context manager - the code inside the scope of the context manager is the job definition.

- `ctx["param"] = "world"` assigns the value "world" to the parameter named "param".
- `ctx["param"]` returns the value of the parameter named "param".
- `ctx.get("param")` returns the value of the parameter named "param" or None, if the parameter is undefined.
- `ctx.get("param", default="default_value")` returns the value of the parameter named "param" it is defined and "default_value" otherwise.
- `"param" in ctx` returns True if the job execution instance contains a parameter named "param", False otherwise.

## Other methods
The job execution instance has a few utility functions:
- `ctx.export("param")` makes the current value of the parameter named "param" available in the environment of subprocesses spawned by robojob.
- `ctx.exit()` exits the job immediately, setting the status of the job to "Completed".
- `ctx.exit(status="Skipped")` exits the job immediately, setting the status of the job to "Skipped".
- `ctx.add_path(path)` adds path to the PATH environment variable available to subprocesses. This is useful when you don't have e.g. RScript.exe in your path in every environment. Any path or list of paths found in the `path` section of robojob.yml will be passed to `add_path` during startup.
- `ctx.add_error_handler(task_execution)` causes `task_execution` to execute as the last task before exiting the job, but only if an (uncaught) exception is raised during job execution.
- `ctx.add_error_email(sender, recipients, subject, content, recipients_cc=[])` adds an email error handler. If the job fails, email will be sent using the SMTP server named in the `smtp_server` context parameter. `subject`and `content` are both treated as [string templates](https://docs.python.org/3/library/string.html#template-strings), with parameter values being substituted for `$name`-style placeholders.


## Configuration

The configuration file is called `robojob.yml` by default, and has the following sections:

- `environment`: The name of the environment.
- `backend`: Backend configuration (TODO: Link to a section on this).
- `path`: Item(s) to the PATH environment variable. Can be a string or a list of strings.
- `parameters`: Parameter object. All attributes of this object will be available as job parameters in all jobs using the configuration.

# Quickstart

Install robojob in a virtual environment like this:

~~~powershell
py -m venv .venv
.\.venv\Scripts\activate
pip install robojob
~~~

## Hello, world

First, try importing robojob and executing a simple Python task.

Save the following as `hello.py` and run it:

~~~python
import robojob

def greet(name):
    print(f"Hello, {name}!")

with robojob.go(job_name="hello") as ctx:
    ctx.execute(greet, name="world")
~~~

The result is the same as calling `greet(name="world")`.

In robojob terms, the `greet()` function is a *task* and the block inside the `with` statement is a *job* (a very simple one that only involves a single task).

Next, turn on logging by adding the following (above the `with` statement):

~~~python
import logging

logging.basicConfig(level="INFO", format="[%(levelname)s] %(message)s")
~~~

Running the script again, you can see the logging output from robojob:

~~~
[INFO] Job starting: <JobExecution: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx>
[INFO] Task starting: <FunctionExecution: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx (greet)>
Hello, world!
[INFO] Task completed with status Completed
[INFO] Running time: 0:00:00.000995
[INFO] Job completed with status Completed
[INFO] Running time: 0:00:00.001995
~~~

<!--
`robojob.go` is a convenience function that returns a `JobExecution` instance that monitors the execution of the code in the `with` block. When execution of the block starts and ends, the `JobExecution` instance will log the time and status of the job execution. Later in this tutorial, we'll use a backend to persist these data in a database.

Inside the `with` block, the `JobExecution` instance can execute a number of different tasks (e.g. Python functions and stored procedures). The time, status and parameter values used in these *task executions* are logged, too.
-->

If you change the log level to "DEBUG" in the call to `basicConfig()` above, you can see the parameter value being assigned, too.

The remainder of the tutorial covers three topics:

- How robojob handles failed tasks and jobs.
- How to use a configuration file to separate parameter values (and other configuration details) from job definitions.
- How to use a backend to log task and job executions to a central location.

## Failure

Try introducing a bug in the job by not passing a value for the `name` parameter:

~~~python
with robojob.go("hello") as ctx:
    ctx.execute(greet)
~~~

The error gets logged along with the stack trace before being reraised:

~~~
[INFO] Job starting: <JobExecution: 339fe025-35db-4195-a6ee-3d9a6b571662>
[ERROR] Job failed: "The parameter 'name' is not defined."
[INFO] Job ended with status Failed
[INFO] Running time: 0:00:00
~~~

Note that the error is reraised at the end of job execution.

Next, add a task that fails:

~~~python
def fail():
    print(1/0)
~~~

Modify the job to call the task:

~~~python
with robojob.go("hello") as ctx:
    ctx.execute(fail)
~~~

Since the `ZeroDivisionError` raised by the task is not caught inside the job, it causes the job to fail.

Both the failure of the task and job are logged ():

~~~
[INFO] Job starting: <JobExecution: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx>
[INFO] Task starting: <FunctionExecution: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx (fail)>
[ERROR] Task failed: division by zero
[INFO] Task completed with status Failed
[INFO] Running time: 0:00:00.000995
[ERROR] Job failed: division by zero
[INFO] Job completed  with status Failed
[INFO] Running time: 0:00:00.003990
Traceback (most recent call last):
  <stack trace>
ZeroDivisionError: division by zero
~~~

You can define a task that is executed when the job fails:

~~~python
def handle_error():
    print(f"Job failed")
~~~

Register the task with the job execution context:

~~~python
with robojob.go("hello") as ctx:
    ctx.add_error_handler(handle_error)
    ctx.execute(fail)
~~~

(Sending email to notify operators of errors can be done with `add_error_email()`, which is not covered in this tutorial.)

## Parameters and configuration files

Until now, we've passed parameter values in the call to execute, like this:

~~~python
with robojob.go(job_name="hello") as ctx:
    ctx.execute(greet, name="world")
~~~

Passing parameters like this is fine for parameters that only apply to one or a few tasks. Some parameters will apply to many (or even most) tasks, and passing these to each and every task is redundant and error-prone.

Defining a parameter at the level of the job makes it available to all subsequent tasks executions:

~~~python
with robojob.go("hello") as ctx:
    ctx["name"] = "world"
    ctx.execute(greet)
~~~

(This produces an extra line of debug logging: `[DEBUG] Setting parameter name = 'world'`)

Robojob inspects the call signature of the function being executed and binds the parameters to values if possible. As we saw above, missing parameters will cause exceptions.

Variables can also be defined as part of job execution initialization:

~~~python
with robojob.go("hello", parameters={"name": "world"}) as ctx:
    ctx.execute(greet)
~~~

Or moved to a YAML configuration file called `robojob.yml`:

~~~yaml
parameters:
  name: world
~~~

This makes the Python code even simpler:

~~~python
with robojob.go("hello") as ctx:
    ctx.execute(greet)
~~~

Separating configuration from code like this lets you move jobs between environments, each with their own parameter values.

### Run-time parameter binding and built-in parameters

If a parameter is added to the task, robojob will try to supply it:

~~~python
def greet(name, job_execution_guid):
    print(f"Hello from job {job_execution_guid}, {name}!")
~~~

Here, the task is asking for the built-in job execution identifier, which is useful for establishing an audit trail.

The `job_execution_guid` parameter is built into robojob. The built-in parameters include:
- `job_execution_guid`: The GUID identifying the currently running job.
- `job_name`: The name of the job.
- `environment_name`: The name of the environment.
- `status`: The current status of the job.
- `error_message`: If the job has failed, this is the error message - this is primarily useful for error handling tasks.

(In addition, backends may provide extra parameter values, like the `job_execution_id` that is provided by the SQL Server backend - more on that below.)

The parameter values listed above cannot be overwritten, as you can see by trying:

~~~python
with robojob.go(job_name="hello") as ctx:
    ctx["job_execution_guid"] = ""
    ctx.execute(greet)
~~~

This still outputs `Hello from hello, world!`.

In the next section, we'll use a backend to provide extra logging capabilites and parameter values.

## Using a backend

All task configuration, execution and orchestration happens through the job execution context, robojob can log job and task executions to a backend.

In this section, we'll try setting up a SQL Server backend to log executions and provide surrogate job execution id's.

First, create a new database to hold the logging tables and a stored procedure that we'll be calling:

~~~sql
CREATE DATABASE Robojob
GO

USE Robojob
GO

CREATE TABLE dbo.JobExecution (
    JobExecutionGUID UNIQUEIDENTIFIER NOT NULL PRIMARY KEY,
    JobExecutionID INT NOT NULL IDENTITY(1,1),
    EnvironmentName NVARCHAR(20) NOT NULL,
    JobName NVARCHAR(255) NOT NULL,
    ExecutedBy SYSNAME NOT NULL DEFAULT SUSER_SNAME(),
    StartedOn DATETIME2(3) NOT NULL,
    CompletedOn DATETIME2(3) NULL,
    [Status] NVARCHAR(20) NULL,
    ErrorMessage NVARCHAR(MAX) NULL,
  )
GO

CREATE TABLE dbo.TaskExecution (
    TaskExecutionGUID UNIQUEIDENTIFIER NOT NULL PRIMARY KEY,
    JobExecutionGUID UNIQUEIDENTIFIER NOT NULL,
    TaskTypeName NVARCHAR(255) NOT NULL,
    TaskName NVARCHAR(255) NOT NULL,
    ExecutedBy SYSNAME NOT NULL DEFAULT SUSER_SNAME(),
    StartedOn DATETIME2(3) NOT NULL,
    CompletedOn DATETIME2(3) NULL,
    [Status] NVARCHAR(20) NOT NULL,
    ErrorMessage NVARCHAR(MAX) NULL,
  )
GO

CREATE TABLE dbo.TaskExecutionParameter (
    TaskExecutionGUID UNIQUEIDENTIFIER NOT NULL,
    ParameterName NVARCHAR(50) NOT NULL,
    ParameterValue NVARCHAR(4000) NOT NULL,
    PRIMARY KEY ( TaskExecutionGUID, ParameterName )
  )
GO

CREATE TABLE dbo.Hello (
    JobExecutionID INT NOT NULL,
    [Message] NVARCHAR(100) NOT NULL
)

GO

CREATE PROCEDURE dbo.Greet @JobExecutionID INT, @Name NVARCHAR(50)
AS
INSERT INTO dbo.Hello (JobExecutionID, [Message])
VALUES (@JobExecutionID, 'Hello ' + @Name)
~~~

Configure the backend in the configuration file:

~~~yaml
backend:
  type: sql server
  connection string: Driver={ODBC Driver 17 for SQL Server};Server=<server name>;Database=Robojob;Trusted_Connection=yes;
~~~

Change the connection string as needed - you must have `pyodbc` installed for this to work.

Running the job again generates logging in the database:

~~~sql
SELECT * FROM dbo.JobExecution;
SELECT * FROM dbo.TaskExecution;
SELECT * FROM dbo.TaskExecutionParameter;
~~~

Finally, we'll try executing a stored procedure. Robojob does not come with a database connection manager, so the job must manage its own connections. Add a parameter called `connection string` to the parameter section of `robojob.yml`:

~~~yaml
parameters:
  name: world
  connection string: Driver={ODBC Driver 17 for SQL Server};Server=<server name>;Database=Robojob;Trusted_Connection=yes;
~~~
The parameter should contain the same connection string as the backend section (normally, the backend would log to a different database than the one the job interacts with, but for demonstrations purposes we're using the same database).

Next, alter the script to import pyodbc, connect to the database and execute a stored procedure:

~~~python
import pyodbc
import robojob
import logging

logging.basicConfig(level="INFO", format="[%(levelname)s] %(message)s")

with robojob.go(job_name="hello") as ctx:
    conn = pyodbc.connect(ctx["connection string"], autocommit=True)
    ctx.execute_procedure(conn, "dbo", "Greet")
~~~

Run it and check the outputs:

~~~sql
SELECT * FROM dbo.Hello;
SELECT * FROM dbo.JobExecution;
SELECT * FROM dbo.TaskExecution;
SELECT * FROM dbo.TaskExecutionParameter;
~~~

Note that the stored procedure is called with `@JobExecutionID`: This is an integer surrogate for the job execution GUID that is allocated by the robojob SQL Server backend and added to the job execution context when job execution begins.

Also, the `@JobExecutionID` is bound to the value of the `job execution id` variable and `@Name` is bound to `name`. This is because parameters are bound by name, ignoring casing and special characters. So:

~~~python
with robojob.go(job_name="hello") as ctx:
    ctx["test value"] = "test"
    print(ctx["test_value"])
    print(ctx["@TestValue"])
    print(ctx["TEST VALUE"])
~~~

## PowerShell tasks

Save the following as `Greet.ps1`:

~~~powershell
param($Name)

"Hello, $Name!" > hello.txt
~~~

If you invoke this from a PowerShell prompt (with `.\Greet.ps1 Dave`) it saves the string "Hello, Dave!" to a file called `hello.txt`

The first line of the script declares the parameters needed by the script. This can be used by robojob to figure out which parameters to pass when invoking the script:

~~~python
import logging

import robojob

logging.basicConfig(level="DEBUG", format="[%(levelname)s] %(message)s")

with robojob.go(job_name="hello") as ctx:
    ctx.execute_powershell("Greet.ps1")
~~~

:warning: Robojob expects to find the entire `param(...)` statement on the first line of the script, and only understands a simple, comma-separated list of parameter names (e.g. `param($one, $two, $three)`), without type declarations or any other supplementary information.

# Other topics

## Returning values from task executions

In general, parameters only flow from robojob to tasks - only exceptions flow the other way.

There's no general way to access the return values of a task execution, but since jobs are defined in Python, any data "left behind" by a task can be queried by the job (e.g. by querying a table just written to by a stored procedure task).

An exception to this rule is Python tasks - since parameter values for these are arbitrary Python objects, you can pass the job execution context itself as a parameter and modify it as part of the task execution.

Here, we're defining a job execution parameter with a dynamic value:

~~~python
import logging
from datetime import date

import robojob

logging.basicConfig(level="DEBUG", format="[%(levelname)s] %(message)s")

def set_date(ctx):
    ctx["today"] = date.today()

with robojob.go(job_name="hello") as ctx:
    ctx.execute(set_date, ctx=ctx)
    print(ctx["today"])

~~~

This could be useful if we wanted to make the calculation and assignment of a parameter visible in the log. Note that the value assigned will not be logged until it is used as a parameter for another task execution, but any inputs to the assignment task will be logged (if we retrieved the value from a file, for instance, the filename could be logged).

## Implementing custom tasks

To implement a custom task, you can derive a class from `TaskExecution`.

You'll need to override `execute()` to do what the task is supposed to do and if the task takes any parameters, you'll need to override `bind_parameters()` as well.

Here's a custom task that downloads a file from the internet:

~~~python
import shutil
import logging

import requests
import robojob
from robojob.task_execution import TaskExecution

logging.basicConfig(level="DEBUG", format="[%(levelname)s] %(message)s")

class WebTask(TaskExecution):
    def bind_parameters(self, context_parameters):
        self.parameters["url"] = context_parameters["url"]
        self.parameters["filename"] = context_parameters["filename"]

    def execute(self):
        response = requests.get(self.parameters["url"], stream=True)
        with open(self.parameters["filename"], 'wb') as outfile:
            shutil.copyfileobj(response.raw, outfile)
        

with robojob.go(job_name="hello") as ctx:
    parameters = {
        "url": "https://imgs.xkcd.com/comics/exploits_of_a_mom.png",
        "filename": "exploits_of_a_mom.png"
        }
    ctx.process_task_execution(WebTask("XKCD"), local_parameters=parameters)
~~~

(You'll need to install `requests` for this to work - note that you'll see logging from `requests` module intermixed with the logging from `robojob`)

The flow of control when this runs goes like this:

1) The `process_task_execution()` method recieves the task execution and (optionally) some local parameters to use when configuring the task execution.
1) It adds the local parameters to the other parameters and passes the resulting parameter collection to the `bind_parameters()` method of the task execution.
1) `bind_parameters()` picks out the parameter values needed by the task and stores them in the `parameters` dictionary. If the `url` or `filename` parameters are missing, a KeyError is raised at this point.
1) Control returns to the `JobExecution` instance, and the fully configured task execution instance is passed to the `before_task_execution()` method of the backend (for logging and whatever else the backend needs to do)
1) The `execute()` method of the task execution is called. Running time and any errors are stored by the task execution instance.
1) The task execution instance is passed to the `after_task_execution()` method of the backend for final logging.

## Leaving early

Sometimes, it makes sense to exit from a job execution before the job has reached the usual end of processing.

For this, you can call the `exit()` method:

~~~python
import logging

import robojob

logging.basicConfig(level="DEBUG", format="[%(levelname)s] %(message)s")

files_to_process = []

with robojob.go(job_name="hello") as ctx:
    if not files_to_process:
        ctx.exit("Skipped") # Nothing to do
    else:
        for file in files_to_process:
            pass # do things to files here
~~~

Exiting like should only be used for non-error exit states like skipping a job execution that has nothing to do. If your code is in an error state and cannot proceed, you should raise an exception.

## Managing large jobs

Suppose you have developed a job that looks like this:

~~~python
import robojob

def task_a(job_name):
    print(f"{job_name} doing task A")

def task_b(job_name):
    print(f"{job_name} doing task B")

with robojob.go(job_name="Job 1") as ctx:
    ctx.execute(task_a)
    ctx.execute(task_b)
~~~

Running this gets us:

~~~
Job 1 doing task A
Job 1 doing task B
~~~

Suppose you have two more jobs that each do two tasks: Job 2 does tasks C and D, job 3 does tasks E and F.

If you wanted to string those three ta



# Interface

## Task execution
The main part of the job execution context interface consists of the methods for executing tasks. A number of convenience methods are provided for this:

- Python functions:
  - `ctx.execute(do_stuff)` executes the python function `dostuff`, binding parameter values by name.
- SQL Server stored procedures:
  - `ctx.execute_procedure(conn, "dbo", "LoadStuff")` executes the stored procedure `dbo.LoadStuff` using the connection `conn`, binding parameters by name (parameter name matching is fuzzy, so the `@` character and casing are both  ignored).
  - `ctx.execute_procedure(conn, "dbo", "LoadStuff", "LoadMoreStuff")` executes two stored procedures in the `dbo` schema.
- R scripts:
  - `ctx.execute_r("DoStuff.R")` executes the script named "DoStuff.R". Parameters are passed by inspecting the first line of the script and looking for parameter names (consisting of letters, numbers and underscores, e.g. `# first_parameter - second_parameter`) and then calling the R script with the value of the named parameters as arguments, in the order listed.
  - `ctx.execute_r("DoStuff.R", "DoMoreStuff.R")` executes two scripts.
- Email:
  - `ctx.send_email(sender, recipients, subject, content)` sends an email. The name of an available SMTP server must be registered in the `smtp_server` context variable. `subject`and `content` are both treated as [string templates](https://docs.python.org/3/library/string.html#template-strings) with parameter values from the job execution context being substituted when the mail is sent.

Note: All these methods call `ctx.process_task_execution(task)` one or more times. Custom tasks can be implemented by subclassing `TaskExecution` and passing instances of the task execution class to `process_task_execution()`. Tasks are also used for error handling: Assigning a task execution instance to `ctx.on_error` will cause the task to be executed immediately before job execution ends, if an error occurs.

