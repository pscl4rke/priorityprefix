

import json
import subprocess
import uuid


def run_into_journald(identifier, filename):
    subprocess.run(f"python3 {filename} 2>&1 | systemd-cat -t {identifier}",
                   shell=True)


def query_journald(identifier):
    result = subprocess.run(f"journalctl -t {identifier} -o json",
                         shell=True, capture_output=True)
    records = []
    for line in result.stdout.decode().splitlines():
        records.append(json.loads(line))
    return records


def check(records, expected):
    for priority, searchfor in expected:
        found = False
        for record in records:
            if searchfor in record["MESSAGE"]:
                found = True
                if int(record["PRIORITY"]) == priority:
                    print("  GOOD %s" % searchfor)
                else:
                    print(" ERROR %s" % searchfor)
        if not found:
            print("ABSENT %s" % searchfor)


def main_logging():
    print("demo-subprocess.py")
    identifier = "priorityprefix-demo-" + str(uuid.uuid4())
    run_into_journald(identifier, "demo-subprocess.py")
    records = query_journald(identifier)
    check(records, [
        (7, "I am a debug"),
        (2, "critical message"),
        (3, "Traceback"),
        (3, ", in h"),
        (3, "ValueError"),
    ])


def main_exception():
    print("demo-exception.py")
    identifier = "priorityprefix-demo-" + str(uuid.uuid4())
    run_into_journald(identifier, "demo-exception.py")
    records = query_journald(identifier)
    check(records, [
        (3, "Traceback"),
        (3, ", in h"),
        (3, "ValueError"),
        (3, "the direct cause of"),
        (3, "Wrapping Exception"),
    ])


if __name__ == "__main__":
    main_logging()
    main_exception()
