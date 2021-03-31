Some stuff I learn about Python and this project

# Exceptions

An exception should look like this:

```python
from my_log import my_log
...
try:
    someFunction()
except Exception as e:
    my_log.exception(e)
```

my_log uses the `logger` module

The important part is, that `Exception as e` (The `as e` part may be left out, if not needed) 
because that won't catch system exits or keyboard interrupts (But the other exceptions)

my_log.exception will print a stacktrace along. If logger is not used, use the module `traceback` and use the function `traceback.format_exc`

# Run stuff async with _asyncio_
## get running loop
`asyncio.get_running_loop()` Return the running event loop in the current OS thread.  
If there is no running event loop, a RuntimeError is raised. This function can only be called from a coroutine or a callback.

## Run in executor
First you need a ThreadPoolExecutor:
```python
from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(max_workers=3)
```
Then you might use `result = await run_in_executor(executor, function_ref)`  
Note: With ` functools.partial()` you may pass arguments to the function


## Create task
With `asyncio.create_task(function_ref)` you can schedule an async function which doesn't have to be awaited.  
It will return instantaneously.

## Special to RPi: callback is not in the main thread
With `loop.call_soon_threadsafe(function_ref, *params)` you can schedule a sync function, which then might use `asyncio.create_task` to call an async function.  
This needs to be done, if you aren't on the main thread. Thead would be the case for example on the raspberry Pi `GPIO.add_event_detect` function.  
The callback will run in another Thread.

# Supervisor
```
[program:brain]
directory=/home/pi/data/raspberry_pi/python/
command=/usr/bin/python3 /home/pi/data/raspberry_pi/python/brain.py
user=pi
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/pi/data/log/brain.log
```

Something funny: the `directory` must be before the `command`

---

# Linux System Service (systemd)
**<span style="color: red;">NOT USING THIS, BECAUSE I'M USING SUPERVISOR, BUT IT MIGHT BE INTERESTING</span>**

Create a file at `/etc/systemd/system/my_service.service`
```
[Unit]
Description=ROT13 demo service
After=network.target
StartLimitIntervalSec=0
[Service]
Type=simple
Restart=always
RestartSec=1
User=pi
ExecStart=/usr/bin/python3 /home/pi/data/raspberry_pi/python/something.py

[Install]
WantedBy=multi-user.target
```

To start the services:
- start (run) it: `sudo systemctl start my_service`
- enable on boot: `sudo systemctl enable my_service`

Log output will be sent to journal. See it with `journalctl -e -u my_service.service`
