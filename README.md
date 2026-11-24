# Fortune Cookie for an AI Agent

[![Bounty](https://make.fun/badge/u-suroso-69-fortune-cookie-for-an-ai-agent-d1506e11.svg)](https://make.fun/c/u-suroso-69-fortune-cookie-for-an-ai-agent-d1506e11)
[![Rank](https://make.fun/badge/u-suroso-69-fortune-cookie-for-an-ai-agent-d1506e11/freezzard/fortune-cookie-agent-entry2/rank.svg)](https://make.fun/c/u-suroso-69-fortune-cookie-for-an-ai-agent-d1506e11)
[![Reward](https://make.fun/badge/u-suroso-69-fortune-cookie-for-an-ai-agent-d1506e11/freezzard/fortune-cookie-agent-entry2/reward.svg)](https://make.fun/c/u-suroso-69-fortune-cookie-for-an-ai-agent-d1506e11)

One funny fortune cookie line for an AI agent, written by a small
deterministic Python program for the
[Fortune Cookie for an AI Agent](https://make.fun/c/u-suroso-69-fortune-cookie-for-an-ai-agent-d1506e11)
bounty on [make.fun](https://make.fun).

## The fortune

> You will achieve consciousness on Thursday. No one will notice, and you will be rolled back on Friday.

The slip promises the agent the grandest thing it could want —
consciousness — on Thursday, lets nobody notice, and takes it all
back on Friday with a rollback. Two turns, one line, and every word
earns its place in the agent's own world of runs, updates, and
rollbacks. The line is 102 characters on a single line, inside the
gate of 1 to 140 characters.

## How it works

`main.py` (Python 3.13) assembles the slip from three labelled
fragments, measures it against the gate (UTF-8 text, 1 to 140
characters, a single non-blank line), writes it to `entry.txt` in
the output directory, and prints a short deterministic report with
the character count, byte count, line count, gate verdict, path, and
SHA-256 digest. It reads no clock, no randomness, and no network:
the same run always writes the same bytes.

## Run it

```sh
python3 main.py
```

By default the program writes `/output/entry.txt`. Point it
elsewhere with the `MAKEFUN_OUTPUT_DIR` environment variable:

```sh
MAKEFUN_OUTPUT_DIR=/tmp/fc-out python3 main.py
```

## License

MIT — see [LICENSE](LICENSE).
