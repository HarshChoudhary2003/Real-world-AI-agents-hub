import time
import json
import psutil
import os
from datetime import datetime

# Configuration (Editable via monitor_input.txt or Dashboard)
THRESHOLD = 80
INTERVAL = 5 # default 
PERSISTENCE = 3

def check_cpu():
    """Returns the current CPU usage percentage."""
    return psutil.cpu_percent(interval=1)

def main():
    print("Initiating Long-Running Monitoring Protocol...")
    consecutive = 0
    log = []
    base_path = os.path.dirname(__file__)
    
    # Path setup
    log_path = os.path.join(base_path, "monitor_log.json")
    alert_path = os.path.join(base_path, "monitor_alert.json")

    try:
        while True:
            cpu = check_cpu()
            timestamp = datetime.utcnow().isoformat()
            entry = {"time": timestamp, "cpu": cpu}
            log.append(entry)

            # Circular log for last 100 entries
            log = log[-100:]

            if cpu > THRESHOLD:
                consecutive += 1
                print(f"[{timestamp}] Threshold Alert Potential: {cpu}% (Consecutive: {consecutive})")
            else:
                consecutive = 0
                print(f"[{timestamp}] Metric Normal: {cpu}%")

            if consecutive >= PERSISTENCE:
                alert = {
                    "alert": "Critical CPU Threshold Exceeded",
                    "time": timestamp,
                    "cpu": cpu,
                    "persistence_reached": PERSISTENCE
                }
                with open(alert_path, "w", encoding="utf-8") as f:
                    json.dump(alert, f, indent=2)
                print("\n" + "!"*40)
                print("CRITICAL ALERT TRIGGERED:", alert)
                print("!"*40 + "\n")
                consecutive = 0  # Reset after alert to detect next sequence

            # Update persistence log
            with open(log_path, "w", encoding="utf-8") as f:
                json.dump(log, f, indent=2)

            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\nMonitoring protocol terminated by operator.")

if __name__ == "__main__":
    main()
