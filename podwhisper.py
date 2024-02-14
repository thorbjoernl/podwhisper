import sys
import os
import time
import requests
import whisper
import json
import pathlib
import logging
from hash import hash
from dotenv import load_dotenv
from pyPodcastParser.Podcast import Podcast
from pathvalidate import sanitize_filename


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

    for i, x in enumerate(podcast.items, start=1):
        logger.info(
            "Processing item " + str(i) + "/" + str(len(podcast.items)) + ": " + x.title
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
        if not already_transcribed:
            if not already_downloaded:
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
                    lines.append(f"**[{s['start']} - {s['end']}]** {s['text'].strip()}")
                    lines.append("")
                f.writelines(lines)

            logger.info("Finishing item.")
        else:
            logger.info("Item already transcribed. Skipping...")

    logger.info("Done!")


if __name__ == "__main__":
    main()
