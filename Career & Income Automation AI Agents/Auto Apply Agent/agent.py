import os

def prepare_application(job_title, company, apply_link):
    """
    Formats the application metadata for tracking or external browser automation.
    """
    return {
        "company": company,
        "role": job_title,
        "apply_link": apply_link,
        "date_prepped": os.getenv("DATE_PREPPED", "Today")
    }

def save_application_track(app_data, status="Ready"):
    """
    Saves the application status to a local file or dashboard.
    """
    import json
    with open("application_history.json", "a") as f:
        log_entry = {**app_data, "status": status}
        f.write(json.dumps(log_entry) + "\n")
    return True
