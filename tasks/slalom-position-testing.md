# slalom-position-testing
- category: comparing

## Setting

```
|b |b |b |b |b |
|k |kD|k |k |k |
|kD|k |k |k |k |
|k |kD|k |k |k |
|kD|k |k |k |k |
|k |kD|k |k |k |
|k |k |kD|k |k |
|k |kD|k |k |k |
|k |k |kD|k |k |
|k |k |k |kD|k |
|k |k |kD|k |k |
|k |k |k |kD|k |
|k |k |k |k |kS|
```

- actionsLimit: 3

## Solution

```
while color() != 'b':
    left()
    if position() > 1:
        left()
    right()
```
