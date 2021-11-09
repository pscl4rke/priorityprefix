

import json
import subprocess
import uuid


def run_into_journald(identifier):
    subprocess.run(f"python3 demo-subprocess.py 2>&1 | systemd-cat -t {identifier}",
                   shell=True)


def query_journald(identifier):
    result = subprocess.run(f"journalctl -t {identifier} -o json",
                         shell=True, capture_output=True)
    records = []
    for line in result.stdout.decode().splitlines():
        records.append(json.loads(line))
    return records


def check(records):
    expected = [
        (7, "I am a debug"),
        (2, "critical message"),
        (3, "Traceback"),
        (3, ", in h"),
        (3, "ValueError"),
    ]
    for priority, searchfor in expected:
        for record in records:
            if searchfor in record["MESSAGE"]:
                if int(record["PRIORITY"]) == priority:
                    print("  GOOD %s" % searchfor)
                else:
                    print(" ERROR %s" % searchfor)


def main():
    identifier = "priorityprefix-demo-" + str(uuid.uuid4())
    run_into_journald(identifier)
    records = query_journald(identifier)
    check(records)


if __name__ == "__main__":
    main()
