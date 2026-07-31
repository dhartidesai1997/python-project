import logging
import os

class AppLogger:
    enabled = False
    level = "WARNING"

    @staticmethod
    def setup(enabled: bool, level: str):
        AppLogger.enabled = enabled
        AppLogger.level = level.upper()

        if not enabled:
            return  # Logging disabled

        os.makedirs("logs", exist_ok=True)

        log_level = logging.INFO if AppLogger.level == "INFO" else logging.WARNING

        logging.basicConfig(
            filename="logs/app.log",
            level=log_level,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

        logging.info(f"Logging enabled with level: {AppLogger.level}")

    @staticmethod
    def log(message: str, level: str = "INFO"):
        if not AppLogger.enabled:
            return

        level = level.upper()
        if level == "INFO":
            logging.info(message)
        else:
            logging.warning(message)
