# unix-epoch

Overshot `git init` a little.

One deliberately backdated commit. Both clocks set to `1970-01-01 00:00:00 UTC`:

```sh
GIT_AUTHOR_DATE='@0 +0000' GIT_COMMITTER_DATE='@0 +0000' \
  git commit --allow-empty -m 'oops, 1970'
```

That's timestamp `0`. The `@` matters for small numbers ([Git docs](https://git-scm.com/docs/git-commit#_date_formats)). Try the command in a throwaway repo.

## Poke the clock

```sh
python experiment.py
```

Needs Python 3 and Git. Reads both date parsers with `git var`; creates no commits and changes no config. [Recorded output](observations.md).

Git `2.55.0.windows.3` accepts `@0 -0800`. Converted at UTC-08:00, that's December 31, 1969. Spell that same instant as `1969-12-31T16:00:00-0800` and Git rejects it. Picky time machine.

The calendar column converts the parsed timestamp using its fixed offset. It doesn't predict GitHub's contribution graph.

## Meanwhile, on GitHub

Checked October 17, 2026 (PDT): [this existing commit](https://github.com/okuoku/the-epoc-repo/commit/e111c81454967d83488272a47c9422c446d6fa65) has both dates at epoch UTC. Its author's graph shows [1 contribution in 1969](https://github.com/users/okuoku/contributions?from=1969-01-01&to=1969-12-31) and [0 in 1970](https://github.com/users/okuoku/contributions?from=1970-01-01&to=1970-12-31).

GitHub [documents](https://docs.github.com/en/account-and-profile/reference/profile-contributions-reference) using the author date and the commit's time zone. Those public records don't explain this year boundary. This repo's graph result is still untested.
