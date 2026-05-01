from datetime import date
from collections import defaultdict

usage = defaultdict(lambda: {"date": "", "count": 0})

def check_and_increment(ip: str) -> bool:
    today = str(date.today())
    if usage[ip]["date"] != today:
        usage[ip] = {"date": today, "count": 0}
    if usage[ip]["count"] >= 3:
        return False
    usage[ip]["count"] += 1
    return True

def get_count(ip: str) -> int:
    today = str(date.today())
    if usage[ip]["date"] != today:
        return 0
    return usage[ip]["count"]