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

- `python pwhisper.py [URL]`

`[URL]` is a url to a podcast rss feed. It will produce a `*.txt`, `*.json` and
a `*.md` file per episode.

- The `text` file is a dump of the generated text without timestamps.
- The `json` file is the segment data produced by Whisper formatted as a json.
- The `md` file is a simple formatted Markdown file, with timestamps.

## Example Output

Here is an example snippet of `*.md` for an episode of
[99 Percent Invisible](https://99percentinvisible.org/):

```
# 99% Invisible - 570- The White Castle System of Eating Houses
**[0.0 - 3.2]** This is 99% Invisible.

**[3.2 - 4.3]** I'm Roman Mars.

**[4.3 - 9.5]** As anyone who has ever been to a White Castle restaurant

**[9.5 - 13.6]** knows the food is, how do I put this?

**[13.6 - 17.2]** It's never going to be considered classic five star food,

**[17.2 - 21.2]** but you know what you're getting when you go there.

**[21.2 - 23.5]** Jeremy Brooks has been a diehard White Castle fan

**[23.5 - 26.8]** ever since going regularly as a kid with his dad.
```
