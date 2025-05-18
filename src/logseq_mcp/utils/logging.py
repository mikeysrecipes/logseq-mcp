import sys
from datetime import datetime


def log(message: str) -> None:
    """Log a message to stderr with a timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}", file=sys.stderr)