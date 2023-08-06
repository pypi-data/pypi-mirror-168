import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger("bs_pathutils")


def ensure_path(path: Path, label: Optional[str]) -> None:
    if not path.exists():
        logger.info("%s path does not exist, creating...", label or path)
        path.mkdir(parents=True)
        if label:
            logger.info("Created %s path @ %s", label, path)
        else:
            logger.info("Created path @ %s", path)
        return
    if label:
        logger.info("Detected %s path @ %s", label, path)
    else:
        logger.info("Detected path @ %s", path)
