# Clock check

`git version 2.55.0.windows.3`

`git var` only: both author and committer paths, no commits created.

Python computes the calendar column from Git's returned timestamp and fixed offset.

| Input | Seconds / offset | Calendar at that offset |
| --- | --- | --- |
| `@0 +0000` | `0 +0000` | `1970-01-01T00:00:00+00:00` |
| `1970-01-01T00:00:00+0000` | `0 +0000` | `1970-01-01T00:00:00+00:00` |
| `0 +0000` | rejected (128) | |
| `1969-12-31T23:59:59+0000` | rejected (128) | |
| `@-1 +0000` | rejected (128) | |
| `@0 -0800` | `0 -0800` | `1969-12-31T16:00:00-08:00` |
| `1969-12-31T16:00:00-0800` | rejected (128) | |
| `@0 +1400` | `0 +1400` | `1970-01-01T14:00:00+14:00` |

Git's complaints:

```text
fatal: invalid date format: 0 +0000
fatal: invalid date format: 1969-12-31T23:59:59+0000
fatal: invalid date format: @-1 +0000
fatal: invalid date format: 1969-12-31T16:00:00-0800
```
