# on-yellow-to-left

## Setting

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
- actionsLimit: 2

## Solution

```python
while color() != 'b':
    fly()
    if color() == 'y':
        left()
```
