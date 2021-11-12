from datetime import datetime


def to_epoch(dt: datetime):
    return int(dt.timestamp() * 1e3)
