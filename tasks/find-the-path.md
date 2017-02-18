# find-the-path
- category: repeat

## Setting

```
|b |b |bA|b |b |
|kM|k |kA|k |kM|
|k |kA|k |kA|k |
|k |kM|kA|k |k |
|kA|k |kM|kA|kA|
|k |k |kM|k |k |
|k |kA|k |kA|k |
|kM|kM|kM|k |kM|
|kA|k |kM|kA|kA|
|k |k |kA|k |k |
|k |k |kS|k |k |
```

- actionsLimit: 4

## Solution

```
repeat 3:
    left()
    shoot()
    fly()
    right()

```
