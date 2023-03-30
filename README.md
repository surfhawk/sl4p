# SL4P : simplest logging for your python

[![](https://img.shields.io/badge/pypi-1.4.2-007ec6?logo=PyPI&logoColor=white)](https://pypi.org/project/sl4p/)
[![](https://img.shields.io/badge/python-Min%203.0%20%7C%20Rec'd%203.6%2B-blue?logo=Python&logoColor=white)](https://pypi.org/project/sl4p/)
[![](https://img.shields.io/badge/license-BSD%20License-lightgrey)](https://pypi.org/project/sl4p/)
[![](https://img.shields.io/badge/build-passing-brightgreen)](https://pypi.org/project/sl4p/)  

**sl4p** is a logging library that makes it easy to introduce more production-focused logging into your python applications.    
sl4p users need not know anything about the slightly complex built-in python logging, although sl4p uses built-in Python's logging internally.  
Quite simply, **you can start logging right in any code with the three lines** below.

```python
from sl4p import *

log = sl4p.getLogger(__file__)
log.info("Hello Sl4p logger !")
```

Then, a log file with the contents below will be created in the folder `./sl4p_logs` in the same location as your code.
```
INFO   | 2023.03.22-17:19:13 - embedding.py (  86) :: OPERATING TIMEZONE: +9:00
INFO   | 2023.03.22-17:19:13 - embedding.py (  87) :: Program  @c8abb11e  started.  <<ex1.py>>
DEBUG  | 2023.03.22-17:19:13 - embedding.py (  88) ::          @@-- argv[0] = C:\path\to\your\python\app.py
INFO   | 2023.03.22-17:19:13 - ex1.py   (   4) :: Hello Sl4p logger !
INFO   | 2023.03.22-17:19:13 - embedding.py ( 105) :: Program  c8abb11e  finished  <<ex1.py>>  -----  Elapsed    0.0010 s
```
Don't waste your time learning logging. Just enjoy this!

## Main Features
Here are the main features that are very easy to use:

**Basic**
- Logging that can be used right away with little to no setup required (by default config)
- ConfigFile: Single/multi-application logger settings by JSON files and python dictionary
- **Auto purging**: log files can be divided and recorded by specified time period or filesize, and old ones can be automatically deleted.
- **Snippet log**: Logging to separate files for specific modules or subset of your Python program package
- **Logging in multi-threaded/multi-process** (internally, without IPC, with recording to a same file)
- Log of program context info: Timezone info, program execution path, total program run time, etc.

**Utils & Advanced**
- **SimpleTimer**: a stopwatch logging utility that supports start and multiple checks
- `@sl4p_time()` records the time taken for function execution (optional user tag)
- `@sl4p_try`, `@sl4p_try_exit` automatically log traceback using Try~Except statements
- **Profiling**: record CPU and memory usage as a separate CSV file during program life
- **ExceptionHook**: Register your function to execute in the event of an abnormal program termination


## Installation
The **'sl4p'** package can be easily installed using pip.
```
$ pip install sl4p
```

Or download the appropriate .whl file for your Python version from the 'dist' folder on GitHub.
```
$ pip install sl4p-{pkg_ver}-{py_ver}-none-any.whl
```

## Configuration (Single App)
Sl4p has key concepts of **'configuration'** and **'logging'**.  
Configuration decides sl4p logger's behavior including logging level, message format, logfile savedir and so on.  
You can use Python dictionary or .cfg Yaml file to configuring as you want. 

The following table describes the available keys and their corresponding values (default values indicated with an asterisk):
```Yaml
# Configured example
{
    "__configver__": "C4",  # For .cfg Yaml file, you must specify __configver__ 

    "LOG": {
        "use_console_print": true,
        "console_level": "WARNING",
        
        "logging_level": "DEBUG",
        "logging_format": "basic",

        "logfile_savedir": "logs",
        "logfile_name": "EXAMPLE_1",
    }
}
```
| Key                 | Description                                                                                                                                       | Available value (*default)                                                                                                                                  |
|---------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `use_console_print` | Whether to print log messages to the console.                                                                                                     | **Bool** (*) True, False                                                                                                                                    |
| `console_level`     | The minimum level of logs to be printed in console.<br/> Logs below this level will not be printed. If not be assigned, follow the logging_level. | (*) "DEBUG", "INFO", "WARNING",  "ERROR", "CRITICAL"                                                                                                        |
| `console_format`    | The level of detail to include in the log message in console.  If not be assigned, follow the logging_format.                                     | "simple", (*) "basic", "detail", "adap"                                                                                                                     |
| `console_stdout`    | Whether to send console output to stdout, otherwise to stderr which is the default of logging. (Output in red text in some IDEs)                  | **Bool** True, (*) False                                                                                                                                    |
| `logging_level`     | The minimum level of logs to be recorded.<br/> Logs below this level will not be recorded.                                                        | (*) "DEBUG", "INFO", "WARNING",  "ERROR", "CRITICAL"                                                                                                        |
| `logging_format`    | The level of detail to include in the log message in file.                                                                                        | "simple", (*) "basic", "detail", "adap"                                                                                                                     |
| `logfile_savedir`   | The absolute path to the directory where log files will be saved. <br/> The path should be in either Windows or Linux format.                     | **String** : The OS-specific folder path <br/>windows ex) "E:\\\\Workspace\\\\sl4p_logs\\\\app-abc" <br/> linux ex) "/opt/my_appvar/data/sl4p_logs/app_abc" |
| `logfile_name`      | The log file name for your application. <br/>(default: based on your python program's name)<br/> Sl4p will use this prefix to identify and purge old log files.                        | **String** : OS-supported filename. <br/> ex) "LOG.your_app_name"                                                                                           |
| `console_colorlog_kwargs` | The dictionary that is passed into initializing colorlog's ColoredFormatter as \*\*kwargs | **Dictionary** (*) colorlog's default (reference: https://github.com/borntyping/python-colorlog) |
| . . . | _There are many other options, see sl4p_examples in this branch._ |
<br/>

## Make logging

### 1. Load your configuration
It is important to load your configuration before using your application. 
I recommend placing this loading config phase at the beginning of your application's main function. 
Please note that this loading phase only needs to be executed once for the entire application package.

When loading your configuration, you can pass your config (dict or Yaml file's path) as second parameter of getLogger().
Additionally, you can use the optional parameter debugprt=True to display sl4p's initialization info.

Here are three ways to load your configuration:


A. **'get-logger' style loading**
```python
log = sl4p.getLogger(__file__, cfg="./applog.cfg", debugprt=True)  #debugprt param is optional!
log.info("hello sl4p!")
```

B. **'with-block' style loading**
```python
with sl4p(__file__, cfg=logcfg_dict) as log:
    log.info("hello sl4p!")
    log.error("Error occured! #%d" % (400))
    # log.error("Error occured! ", 400)  --> Not support this 'print()' style, Please formatting.
```

C. **How to load logger in Jupyter**  
`__file__`, the first argument of getLogger, is used as an identifier in Snippet logging.  
Instead, enter any string in Jupyter.
```python
log = sl4p.getLogger('jupyter', cfg=logcfg_dict):
log.info('Hello sl4p in jupyter!')
```

<br/>

### 2. Write a log message
After loading your configuration, you can log messages anywhere in your application, even in another file or modules, without passing the second parameter into getLogger.  
Here are two ways to use logging:

A. **'get-logger' style logging**
```python
log = sl4p.getLogger(__file__)
log.debug("Just pass only __file__")
```

B. **'with-block' style logging**
```python
with sl4p(__file__) as log:
    log.warning("warn msg! : you should not pass 2nd parameter to sl4p() after configuration completed")
```
<br/>

That's it! Enjoy logging your application :)  
Remember to load your configuration only once (initial entry-point, recommended) and log your messages everywhere !

<br/>



## Utils & Advanced

The 'with-block' logging feature can measure elapsed time as DEBUG log and can also include a custom tag using `tag={TAG_NAME}`.  
Here is an example:

```python
import time
with sl4p(__file__, tag='myTag') as log:
    time.sleep(1.0)
    log.info('with-block time measuring and tagging feature!')
```
This is the output log:
```text
DEBUG  | 2019.11.14-22:03:43 - example2.py #myTag @adfd08e4 started
INFO   | 2019.11.14-22:03:44 - with-block time measuring and tagging feature!
DEBUG  | 2019.11.14-22:03:44 - example2.py #myTag @adfd08e4 finished  ----  Elapsed    1.0001 s
```
<br/>

**Decorator - @sl4p_time(tag={TAG_NAME})**<br/>
You can also use the `@l4p_time(tag={TAG_NAME})` decorator to measure the execution time of a function and log it with DEBUG level:
```python
@sl4p_time()  # Although you do not use tagging, l4p_time decorator must be written with () brackets.
def my_function1():
    time.sleep(1.5)
    log.error('not yet...')
```
This is the output log:
```text
DEBUG  | 2019.11.14-22:12:43 - example3.py f`my_function1() @19f19de9 started
ERROR  | 2019.11.14-22:12:44 - not yet...
DEBUG  | 2019.11.14-22:12:44 - example3.py f`my_function1 @19f19de9 finished  ----  Elapsed    1.5038 s
```
<br/>

**Decorator - @sl4p_try, @sl4p_try_exit**<br/>
you can use the `@sl4p_try` and `@sl4p_try_exit` decorator to try-except your function and log the traceback of the exception.
```python
@sl4p_try
def take_exception():
    a = 'ABCD' + None
```
This is the output log:
```text
ERROR  | 2019.11.14-22:12:44 - can only concatenate str (not "NoneType") to str
Traceback (most recent call last):
  File "D:\Devel_Workspace\py27_9\devel_logger\sl4p\decorators.py", line 21, in wrapped
    return func(*args, **kwargs)
  File "D:/Devel_Workspace/py27_9/devel_logger/example3.py", line 15, in take_exception
    a = 'ABCD' + None
TypeError: can only concatenate str (not "NoneType") to str
```
Remember `@sl4p_try` will continue the program when excepted, but `@sl4p_try_exit` will terminate it.
<br/><br/>


## About
### Dependencies
* json
* psutil
* colorlog
* pywin32 _(only in windows)_
* colorama _(only in windows)_

### License
BSD 3

### Getting Help / Discussion / Contributing
Right here, please be active in this GitHub repository.  
All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.  
<br/>

***
## Release Note

**(*) ver 1.4.2 :: Coloring console log (by colorlog) and add related configs, Support console stdout'**  
ver 1.4.1 :: Correct the docs, Change default config (console config has no initial values)  
ver 1.4.0 :: Layered apps-config, Support console level&format, IndLogger, Enhance stability  
ver 1.3.3linux :: excluding 'psutil' in requires for linux   
ver 1.3.3 :: override_dict bugfix (support python 3.9+)  
ver 1.3.2 :: Add log_level for SimpleTimer: logger.create_simpleTimer(), config bugfix  
ver 1.3.1 :: Add log_level for @sl4p_time decorator  
ver 1.2.0 :: Add stopwatch(SimpleTimer), Profiling stats(CPU & MEM), Recording TimeZone  
ver 1.0.1 :: Supports multi-byte msg, update config and constants / Patch debugprt, start_ts  
ver 1.0.0 :: First deployed release version  
