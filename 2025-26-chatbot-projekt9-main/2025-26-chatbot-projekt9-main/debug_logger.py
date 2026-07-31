# debug_logger.py
class DebugLogger:
    enabled = False

    @classmethod
    def log(cls, msg):
        if cls.enabled:
            print(f"[DEBUG] {msg}")