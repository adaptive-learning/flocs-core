# clean-your-path
- category: repeat

## Setting

```
|b |b |b |b |b |b |b |
|kW|kM|kA|k |k |k |k |
|k |k |kM|kA|k |k |k |
|k |k |k |kM|kA|k |k |
|k |k |k |k |kM|kA|k |
|k |k |k |k |k |kM|kA|
|k |k |k |k |k |k |kD|
|k |k |k |k |k |k |kW|
|k |k |k |k |k |k |k |
|k |k |k |k |k |k |k |
|k |k |k |k |k |k |k |
|k |k |k |k |k |kS|k |
```

- actionsLimit: 5

## Solution

```
repeat 5:
    shoot()
    left()
fly()
repeat 6:
    left()
```