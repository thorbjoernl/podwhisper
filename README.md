# Podcast whisper

A script for running each episode in a podcast rss through [Whisper](https://github.com/openai/whisper)
to transcribe the podcast.

Configure it using the `.env` file. `WHISPER_MODEL` can be any of the options described
[here](https://github.com/openai/whisper?tab=readme-ov-file#available-models-and-languages).

## Installation

- Clone the repository.
- `poetry install`
- `poetry shell`

## Running the program

- `python pwhisper.py [URL]`

`[URL]` is a url to a podcast rss feed. It will produce a `*.txt`, `*.json` and
a `*.md` file per episode.

- The `text` file is a dump of the generated text without timestamps.
- The `json` file is the segment data produced by Whisper formatted as a json.
- The `md` file is a simple formatted Markdown file, with timestamps.

## Example Output

Here is an example snippet of `*.md` for the most recent episode of
[Hello Internet](https://www.hellointernet.fm/):

```

```
