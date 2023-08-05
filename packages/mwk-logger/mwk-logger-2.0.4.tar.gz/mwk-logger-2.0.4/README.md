
# MWK logger

---
[![PyPI](https://img.shields.io/pypi/v/mwk-logger)](https://pypi.org/project/mwk-logger/)  
**Custom logger with colors on terminal.**  
![logger](https://user-images.githubusercontent.com/105928466/190899542-94a70a4d-ef1a-418a-90be-0143d3d1d630.JPG)  
**And some useful decorators.**  
![dec](https://user-images.githubusercontent.com/105928466/190899507-cfcefe55-b21a-4d3b-ae85-bce418121366.JPG)  
![dec_log](https://user-images.githubusercontent.com/105928466/190899529-b147e76a-29f1-4383-9670-b24fbc02e4a5.JPG)  

---

## Installing package

```
pip install mwk-logger
```

---

## Using logger

### 1. Get instance of mwk-logger
```python
from mwk_logger import MwkLogger

log = MwkLogger(name='mwk',
                file='logger.log',
                stream_level='DEBUG',
                file_level='DEBUG',
                time=True)
```

*keyword parameters:*  
- *name* - name of the logger, by default = 'mwk',
- *file* - path to file to log into, by default = 'mwk.log',
- *stream_level* - logging level for terminal, by default = 'WARNING',
- *file_level* - logging level for file, by default = None,
- *time* - if timestamp should be added to terminal log, by default = False,

LEVELS:
 **None** - no logging or:  
 '**DEBUG**', '**INFO**', '**WARNING**', '**ERROR**', '**CRITICAL**'.  
If both levels are set to **None** stream_level is changed to **WARNING**.  
Timestamp is always added to file logs. One can set if timestamp will be added to terminal logs.  

### 2. Logging  
```python
log.debug('This is a debug message.')
log.info('This is an info message.')
log.warning('This is a warning message.')
log.error('This is an error message!')
log.critical('This is a critical message!!!')
log.exception('This is an exception message!')
```

---

## Using decorators
1. **@timer** - print or log the runtime of the decorated function
2. **@f_sig** - print or log the signature and the return value of the decorated function  
### 1. Decorator with no arguments
Prints on screen.  
```python
from mwk_logger import timer, f_sig

@timer
@f_sig
def function(*args, **kwargs):
    # ... some function ...
    return 'something'
```

### 1. Decorator with arguments
Output is logged with provided logger with level = **INFO**.  
!!! keyword ***logger*** is obligatory !!!
```python
from mwk_logger import MwkLogger, timer, f_sig

log = MwkLogger()

@timer(logger=log)
@f_sig(logger=log)
def function(*args, **kwargs):
    # ... some function to be logged...
    return 'something'
```

---

