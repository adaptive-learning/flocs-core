Setting
-------

```
|b |b |b |b |b |
|k |kA|kA|kA|kA|
|kA|y |k |k |k |
|k |k |k |k |k |
|k |k |k |k |k |
|k |k |kA|kA|kA|
|kA|kA|y |k |k |
|k |k |k |k |k |
|k |k |kS|k |k |
```

Solution
--------

```python
while color() != 'b':
    fly()
    if color() == 'y':
        left()
```
