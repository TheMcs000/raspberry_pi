Some stuff I learn about Python and this project

# Exceptions

An exception should look like this:

```python
try:
    someFunction()
except Exception as e:
    my_log.exception(e)
```

The important part is, that `Exception as e` (The `as e` part may be left out, if not needed) 
because that won't catch system exits or keyboard interrupts (But the other exceptions)
