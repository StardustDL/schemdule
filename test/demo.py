from datetime import datetime, timedelta

now = datetime.now()
now = now - timedelta(microseconds=now.microsecond)


def callable_payload():
    print("From Callable")


def callable_payload2(value):
    def internal():
        print(f"From Callable for resting (cycle {value}).")
    return internal


at((now + timedelta(seconds=1)).time(), "Demo event", callable_payload)

at((now + timedelta(seconds=3)).time(), "Demo event")

cycle((now + timedelta(seconds=5)).time(),
      (now + timedelta(seconds=20)).time(),
      "00:00:05",
      "00:00:05",
      "Demo cycle",
      None,
      lambda i: payloads().use(callable_payload2(i)))

prompter.clear().useSwitcher().useConsole().useCallable()
