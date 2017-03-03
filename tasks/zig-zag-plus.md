# zig-zag-plus
- category: loops

## Setting

```
|b |b |b |b |b |
|kA|k |kA|k |kA|
|k |kA|k |kA|k |
|kA|k |kA|k |kA|
|k |kA|kM|kA|k |
|kA|k |kA|k |kA|
|kM|kA|k |kA|kM|
|kA|k |kA|k |kA|
|k |kA|k |kA|k |
|kA|k |kA|k |kA|
|k |kA|k |kA|k |
|kA|k |kA|k |kA|
|k |k |kS|k |k |
```

- actionsLimit: 4

## Solution

```
repeat 2:
    right()
repeat 3:
    left()
repeat 3:
    right()
repeat 5:
    left()

```
