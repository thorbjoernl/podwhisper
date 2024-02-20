import sys
import os
import time
import requests
import statistics
import whisper
import json
import pathlib
import logging
from hash import hash
from dotenv import load_dotenv
from pyPodcastParser.Podcast import Podcast
from pathvalidate import sanitize_filename


def timestampstr_from_seconds(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    sec = int((seconds % 3600) % 60)

    return f"{str(hours).rjust(2, '0')}:{str(minutes).rjust(2, '0')}:{str(round(sec, 1)).rjust(2, '0')}"


def main():
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))

    if len(sys.argv) < 2:
        logger.error("Missing URL. Aborting.")
        exit()

    feed_url = sys.argv[1]

    logger.info("Processing feed: " + feed_url)

    load_dotenv()
    model_name = os.getenv("WHISPER_MODEL")

    logger.info("Whisper model used: " + model_name)

    model = whisper.load_model(model_name)

    try:
        podcast = Podcast(requests.get(feed_url).content)
    except requests.exceptions.ConnectionError as e:
        logger.error(e)
    except requests.exceptions.HTTPError as e:
        logger.error(e)

    if not os.path.exists(os.path.join("tmp", sanitize_filename(podcast.title))):
        os.makedirs(os.path.join("tmp", sanitize_filename(podcast.title)))

    if not os.path.exists(os.path.join("out", sanitize_filename(podcast.title))):
        os.makedirs(os.path.join("out", sanitize_filename(podcast.title)))

    timings = []
    for i, x in enumerate(podcast.items, start=1):
        start_time = time.perf_counter()
        logger.info(f"Processing item {i}/{len(podcast.items)}: {x.title}")

        if len(timings) > 0:
            logger.info(
                f"ETA: {(len(podcast.items)-i+1)*statistics.mean(timings):.2f} seconds"
            )

        audio_url = x.enclosure_url
        file_extension = pathlib.Path(audio_url).suffix

        # Paths for intermediary and output files.
        audio_path = os.path.join(
            "tmp",
            sanitize_filename(podcast.title),
            hash(x.guid + x.title) + file_extension,
        )
        text_path = os.path.join(
            "out", sanitize_filename(podcast.title), sanitize_filename(x.title + ".txt")
        )
        segment_path = os.path.join(
            "out",
            sanitize_filename(podcast.title),
            sanitize_filename(x.title + ".json"),
        )
        timestamped_path = os.path.join(
            "out", sanitize_filename(podcast.title), sanitize_filename(x.title + ".md")
        )

        already_transcribed = (
            os.path.exists(text_path)
            and os.path.exists(segment_path)
            and os.path.exists(timestamped_path)
        )
        already_downloaded = os.path.exists(audio_path)

        # Download if necessary.
        if not already_transcribed and not already_downloaded:
            logger.info("Downloading...")
            while True:
                r = requests.get(audio_url)
                if r.status_code == 200:
                    break
                logger.warning("Download failed. Retrying in 1 second...")
                time.sleep(1)
            with open(audio_path, "wb") as f:
                f.write(r.content)
        else:
            logger.info("Audio exists. Skipping download...")

        # Transcribe.
        if not already_transcribed:
            logger.info("Transcribing...")
            result = model.transcribe(audio_path)

            # Output raw text.
            with open(text_path, "w") as f:
                f.write(result["text"])

            # Output segments.
            with open(segment_path, "w") as f:
                json.dump(result["segments"], f, indent=4)

            # Timestamp formatted.
            with open(timestamped_path, "w") as f:
                lines = [f"# {podcast.title} - {x.title}"]
                for s in result["segments"]:
                    lines.append(
                        f"**{timestampstr_from_seconds(s['start'])}** {s['text'].strip()}"
                    )
                    lines.append("")
                f.write("\n".join(lines))

            logger.info("Finishing item.")
        else:
            logger.info("Item already transcribed. Skipping...")

        logging.info(
            f"Episode processed in {time.perf_counter()-start_time:.2f} seconds."
        )
        timings.append(time.perf_counter() - start_time)
    logger.info("Done!")


if __name__ == "__main__":
    main()
