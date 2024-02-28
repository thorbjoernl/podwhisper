# Podcast whisper

A script for running each episode in a podcast rss through [Whisper](https://github.com/openai/whisper)
to transcribe the podcast.

Configure it using the `.env` file. `WHISPER_MODEL` can be any of the options described
[here](https://github.com/openai/whisper?tab=readme-ov-file#available-models-and-languages).

## Installation

Poetry is required for installation.

- Clone the repository.
- `poetry install` to install dependencies.
- `poetry shell` to activate the virtual environments.

## Running the program

- `python podwhisper.py [URL]`

`[URL]` is a url to a podcast rss feed. It will produce a `*.txt`, `*.json` and
a `*.md` file per episode.

- The `text` file is a dump of the generated text without timestamps.
- The `json` file is the segment data produced by Whisper formatted as a json.
- The `md` file is a simple formatted Markdown file, with timestamps.

## Example Output

Here is an example snippet of `*.md` for an episode of
[99 Percent Invisible](https://99percentinvisible.org/):

```
# 99% Invisible - 438- The Real Book [rebroadcast]
**00:00:00** This is 99% Invisible. I'm Roman Mars.

**00:00:06** Since the mid-1970s, almost every jazz musician has owned a copy of the same book. It has

**00:00:12** a peach-colored cover, a chunky 70s-style logo, and black plastic binding. It is delightfully

**00:00:19** homemade-looking, like it was printed by a bunch of teenagers at Kinko's. And inside

**00:00:24** is the sheet music for hundreds of common jazz tunes, also known as jazz standards,

**00:00:31** all meticulously notated by hand. It's called The Real Book.

**00:00:36** When I started playing jazz, I remember the first thing my guitar teacher said was, well,

**00:00:40** you gotta buy a real book.

**00:00:42** That's producer Michael McAvanot.

**00:00:44** Everybody had one. It just felt like something you were expected to own if you were a serious

**00:00:49** musician. My high school jazz teacher, Mr. Leonard, had stacks of real books on his desk.

**00:00:53** And he told me that he actually got his first real book at the place where they were originally

**00:00:58** published, Berkeley College of Music in Boston. He had just arrived for his freshman year.
```
