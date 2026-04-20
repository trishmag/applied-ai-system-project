# logger.py
# Sets up a file-based logger to record all game events for debugging and auditing.

import logging


def setup_logger(log_file: str = "game_log.txt") -> logging.Logger:
    """
    Creates and returns a logger that writes to game_log.txt.
    Safe to call multiple times — will not add duplicate handlers.
    """
    logger = logging.getLogger("glitch_investigator")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger


def log_event(logger: logging.Logger, event_type: str, details: dict) -> None:
    """
    Logs a structured game event.
    event_type examples: GAME_START, GUESS, WIN, LOSS, AI_COACH_CALLED
    """
    detail_str = " | ".join(f"{k}={v}" for k, v in details.items())
    logger.info(f"EVENT={event_type} | {detail_str}")
