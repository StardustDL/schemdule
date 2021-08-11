from datetime import datetime, timedelta
now = datetime.now()
now = now - timedelta(microseconds=now.microsecond)

def callable_payload():
    print("From Callable")

at((now + timedelta(seconds=1)).time(), "Demo event", callable_payload)

at((now + timedelta(seconds=3)).time(), "Demo event")

cycle((now + timedelta(seconds=5)).time(), 
    (now + timedelta(seconds=20)).time(),
    "00:00:05",
    "00:00:05", "Demo cycle")

prompter.clear().useSwitcher().useConsole().useCallable()
