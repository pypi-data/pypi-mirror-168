from datetime import datetime


def convert_timestamp(value):
    if isinstance(value, datetime):
        return value
    elif isinstance(value, str):
        return datetime.fromisoformat(value)
