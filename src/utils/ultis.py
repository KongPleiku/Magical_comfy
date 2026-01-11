from loguru import logger
import os
import csv
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent


IMAGE_SRC = "https://picsum.photos/1080/1920"


def load_danbooru_tags():
    """Loads tags from the danbooru.csv file."""
    tags = []
    assets_dir = os.getenv("ASSETS_DIR", "assets")
    logger.info(f"Assets directory: {assets_dir}")
    # Updated path to storage/data/danbooru.csv
    file_path = os.path.join(ROOT_DIR, "assets", "tags", "all_tags.csv")
    logger.info(f"Loading danbooru tags from {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if row:
                    # Assuming the tag is in the first column
                    tags.append(row[0])
        logger.info(f"Loaded {len(tags)} tags.")
    except FileNotFoundError:
        logger.error(
            f"Error: {file_path} not found. Please check the directory structure.",
            exc_info=True,
        )
    return tags


ALL_TAGS = load_danbooru_tags()
