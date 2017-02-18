# zig-zag

## Setting

```
|b |b |b |b |b |
|kA|k |kA|k |kA|
|k |kA|k |kA|k |
|kA|k |kA|k |kA|
|k |kA|k |kA|k |
|kA|k |kA|k |kA|
|k |kA|k |kA|k |
|kA|k |kA|k |kA|
|k |k |kS|k |k |
```
- actionsLimit: 2

## Solution

```python
while color() != 'b':
    right()
    left()
```
