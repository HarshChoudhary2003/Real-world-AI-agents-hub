import csv
import json
from datetime import datetime, timedelta, date

PRIORITY_RULES = {
    "high": [7, 3, 1, 0],
    "medium": [3, 1],
    "low": [1]
}

def parse_date(s):
    return datetime.strptime(s, "%Y-%m-%d").date()

def generate_reminder_times(deadline, priority):
    days_before = PRIORITY_RULES.get(priority, [])
    times = []
    for d in days_before:
        reminder_date = deadline - timedelta(days=d)
        if reminder_date >= date.today():
            times.append(reminder_date)
    return times

def read_tasks(path="tasks.csv"):
    tasks = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tasks.append({
                "task": row["task"],
                "deadline": parse_date(row["deadline"]),
                "priority": row["priority"].lower(),
                "context": row.get("context", "")
            })
    return tasks

def build_reminders(tasks):
    reminders = []
    for t in tasks:
        times = generate_reminder_times(t["deadline"], t["priority"])
        for r_date in times:
            reminders.append({
                "task": t["task"],
                "context": t["context"],
                "priority": t["priority"],
                "deadline": t["deadline"].isoformat(),
                "remind_on": r_date.isoformat(),
                "message": f"Reminder: '{t['task']}' is due on {t['deadline']}."
            })
    reminders.sort(key=lambda r: r["remind_on"])
    return reminders

def main():
    try:
        tasks = read_tasks()
    except FileNotFoundError:
        print("tasks.csv not found!")
        return

    reminders = build_reminders(tasks)

    with open("reminders.json", "w", encoding="utf-8") as f:
        json.dump(reminders, f, indent=2)

    with open("reminders.txt", "w", encoding="utf-8") as f:
        f.write("Smart Reminder Schedule\n")
        f.write("=" * 40 + "\n\n")
        for r in reminders:
            f.write(f"{r['remind_on']} -> {r['message']}\n")

    print("Smart reminders generated.")
    print(f"Total reminders: {len(reminders)}")

if __name__ == "__main__":
    main()
