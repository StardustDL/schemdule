from datetime import datetime, time, timedelta

BASE_DATETIME = datetime(2000, 1, 1)


def to_timedelta(value: time) -> timedelta:
    return timedelta(hours=value.hour, minutes=value.minute,
                     seconds=value.second, microseconds=value.microsecond)


def subtract_time(a: time, b: time) -> timedelta:
    return to_timedelta(a) - to_timedelta(b)

def parse_time(value: str) -> time:
    time(*list(map(int, map(round, map(float, value.split(':'))))))