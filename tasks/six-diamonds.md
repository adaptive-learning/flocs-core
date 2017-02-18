# six-diamonds
- category: final-challenge

## Setting

```
|b |b |b |b |
|k |k |kW|k |
|k |kD|kD|k |
|k |kD|kD|k |
|k |kD|kD|k |
|kS|k |k |kW|
```

- actionsLimit: 2

## Solution

```
while color() != 'b':
    if position() < 3:
        right()
    else:
        left()
```
