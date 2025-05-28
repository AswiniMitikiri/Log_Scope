import re
from dateutil import parser as date_parser


def parse_access_log(filepath):
    pattern = r'(?P<ip>\S+) - - \[(?P<timestamp>[^\]]+)\] "(?P<method>\S+) (?P<path>.*?) \S+" (?P<status>\d{3}) (?P<size>\d+)'
    results = []
    with open(filepath, "r") as file:
        for line in file:
            match = re.match(pattern, line)
            if match:
                results.append(match.groupdict())
    return results


def parse_error_log(filepath):
    pattern = r"\[(?P<timestamp>.+?)\] \[(?P<level>\w+)\] (?P<message>.*)"
    results = []
    with open(filepath, "r") as file:
        for line in file:
            match = re.match(pattern, line)
            if match:
                results.append(match.groupdict())
    return results


def parse_fallback(filepath):
    results = []
    with open(filepath, "r") as file:
        for line in file:
            clean = line.strip()
            timestamp = None
            # Match Linux-style syslog timestamp like "Jun 14 15:16:01"
            try:
                match = re.match(r'^([A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})', clean)
                if match:
                    timestamp = date_parser.parse(match.group(1), fuzzy=True)
            except Exception:
                pass
            results.append({
                "timestamp": str(timestamp) if timestamp else None,
                "message": clean
            })
    return results
