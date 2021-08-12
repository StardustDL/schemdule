from datetime import timedelta


class GlobalConfiguration:
    def __init__(self) -> None:
        self.timeslice: timedelta = timedelta(seconds=1)


globalConfiguration = GlobalConfiguration()
