# diamonds-on-yellow
- category: if-else

## Setting

```
|b |b |b |b |b |
|k |yD|k |k |k |
|k |k |yD|k |k |
|k |k |k |k |k |
|k |k |k |k |k |
|k |yD|k |k |k |
|k |k |yD|k |k |
|k |k |k |yD|k |
|k |k |k |k |k |
|k |k |k |k |k |
|k |k |yD|k |k |
|k |k |k |yS|k |
```

- actionsLimit: 2

## Solution

```
while color() != 'b':
    if color() == 'y':
        left()
    else:
        right()
```