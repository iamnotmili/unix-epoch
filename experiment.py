#!/usr/bin/env python3
"""Ask Git how it reads dates. No commits, config writes, or network calls."""

import os
import re
import subprocess
from datetime import datetime, timedelta, timezone


DATES = (
    "@0 +0000",
    "1970-01-01T00:00:00+0000",
    "0 +0000",
    "1969-12-31T23:59:59+0000",
    "@-1 +0000",
    "@0 -0800",
    "1969-12-31T16:00:00-0800",
    "@0 +1400",
)
EPOCH = datetime(1970, 1, 1, tzinfo=timezone.utc)


def git(*args, env=None):
    return subprocess.run(
        ["git", "--no-optional-locks", *args],
        env=env, capture_output=True, text=True, check=False,
    )


def inspect(date, role):
    env = os.environ.copy()
    env.update({
        f"GIT_{role}_NAME": "Time traveller",
        f"GIT_{role}_EMAIL": "clock@example.invalid",
        f"GIT_{role}_DATE": date,
        "LC_ALL": "C",
    })
    result = git("var", f"GIT_{role}_IDENT", env=env)
    if result.returncode:
        return None, result.returncode, result.stderr.strip()
    match = re.fullmatch(r"Time traveller <clock@example\.invalid> (-?\d+) ([+-]\d{4})", result.stdout.strip())
    if match is None:
        raise RuntimeError(f"Unexpected Git identity: {result.stdout!r}")
    return match.groups(), 0, ""


def main():
    version = git("--version")
    if version.returncode:
        raise RuntimeError(version.stderr.strip())
    print(f"# Clock check\n\n`{version.stdout.strip()}`\n")
    print("`git var` only: both author and committer paths, no commits created.\n")
    print("Python computes the calendar column from Git's returned timestamp and fixed offset.\n")
    print("| Input | Seconds / offset | Calendar at that offset |")
    print("| --- | --- | --- |")
    errors = []
    for date in DATES:
        author = inspect(date, "AUTHOR")
        committer = inspect(date, "COMMITTER")
        if author != committer:
            raise RuntimeError(f"Author/committer disagree for {date!r}: {author!r}, {committer!r}")
        parsed, code, error = author
        if parsed is None:
            print(f"| `{date}` | rejected ({code}) | |")
            errors.append(error)
            continue
        seconds, offset = parsed
        minutes = (int(offset[1:3]) * 60 + int(offset[3:])) * (-1 if offset[0] == "-" else 1)
        calendar = (EPOCH + timedelta(seconds=int(seconds))).astimezone(timezone(timedelta(minutes=minutes)))
        print(f"| `{date}` | `{seconds} {offset}` | `{calendar.isoformat()}` |")
    if errors:
        print("\nGit's complaints:\n\n```text\n" + "\n".join(errors) + "\n```")


if __name__ == "__main__":
    main()
