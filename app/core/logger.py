from loguru import logger
import sys
import os


def setup_logger():
    logger.remove()  # Remove default logger

    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)

    # Add a stdout logger with a simple format
    logger.add(
        sys.stdout,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level="INFO",
    )

    # Add a file logger with JSON format for structured logging
    logger.add("logs/app.log", rotation="1 week", serialize=True, level="DEBUG")

    # Optionally, add a separate error log file
    logger.add(
        "logs/errors.log",
        rotation="1 week",
        level="ERROR",
        backtrace=True,
        diagnose=True,
    )


setup_logger()

# The 'logger' instance is now globally available
