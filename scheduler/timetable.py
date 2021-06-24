from datetime import date, time, datetime
from .prompters import Prompter
import functools


@functools.total_ordering
class TimeTableItem:
    def __init__(self, time: time, message: str = "") -> None:
        self.time = time
        self.message = message

    def __eq__(self, other: object) -> bool:
        if isinstance(other, TimeTableItem):
            return (self.time, self.message) == (other.time, other.message)
        return NotImplemented

    def __lt__(self, other: object) -> bool:
        if isinstance(other, TimeTableItem):
            return self.time < other.time
        return NotImplemented

    def __repr__(self) -> str:
        return f"TimeTableItem({self.time}, {self.message})"


class TimeTable:
    def __init__(self) -> None:
        self.items: list[TimeTableItem] = []

    def at(self, time: time, message: str = "") -> None:
        self.items.append(TimeTableItem(time, message))


def schedule(schema: TimeTable) -> None:
    items = list(sorted(schema.items))

    prompter: Prompter

    from .prompters.general import TkinterPrompter
    prompter = TkinterPrompter()

    print(items)
    prompter.prompt("abc")


def timetable_from_source(src: str) -> TimeTable:
    result = TimeTable()

    def at(time_str: str, message: str):
        pars = list(map(int, time_str.split(':')))
        result.at(time(*pars), message)

    eval(src, {"at": at})

    return result
