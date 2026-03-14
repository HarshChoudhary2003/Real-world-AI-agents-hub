import csv
import json
from datetime import datetime, timedelta

WORKDAY_START = "09:00"
WORKDAY_END = "17:00"
BUFFER_MINUTES = 10

PRIORITY_ORDER = {"high": 1, "medium": 2, "low": 3}

def parse_time(s):
    return datetime.strptime(s, "%H:%M")

def read_tasks(path="tasks.csv"):
    tasks = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tasks.append({
                "task": row["task"],
                "effort": int(row["effort_minutes"]),
                "priority": row["priority"].lower()
            })
    return tasks

def generate_schedule(tasks):
    # Sort tasks primarily by explicit priority string mapping, then linearly by the heaviest tasks first
    tasks.sort(key=lambda t: (PRIORITY_ORDER.get(t["priority"], 3), -t["effort"]))

    current_time = parse_time(WORKDAY_START)
    end_time = parse_time(WORKDAY_END)
    schedule = []
    overflow = []

    for t in tasks:
        block_end = current_time + timedelta(minutes=t["effort"])
        if block_end <= end_time:
            schedule.append({
                "task": t["task"],
                "start": current_time.strftime("%H:%M"),
                "end": block_end.strftime("%H:%M"),
                "priority": t["priority"],
                "duration": t["effort"]
            })
            current_time = block_end + timedelta(minutes=BUFFER_MINUTES)
        else:
            overflow.append(t)

    return schedule, overflow

def main():
    try:
        tasks = read_tasks()
    except FileNotFoundError:
        print("tasks.csv not found")
        return
        
    schedule, overflow = generate_schedule(tasks)

    with open("schedule.json", "w", encoding="utf-8") as f:
        json.dump({
            "schedule": schedule,
            "overflow": overflow
        }, f, indent=2)

    with open("schedule.txt", "w", encoding="utf-8") as f:
        f.write("Daily Time-Blocked Schedule\n")
        f.write("=" * 40 + "\n\n")
        for b in schedule:
            f.write(f"{b['start']}-{b['end']}: {b['task']}\n")

        if overflow:
            f.write("\nUnscheduled Tasks:\n")
            for t in overflow:
                f.write(f"- {t['task']}\n")

    print("Time-blocking plan generated.")
    print(f"Scheduled blocks: {len(schedule)}")

if __name__ == "__main__":
    main()
