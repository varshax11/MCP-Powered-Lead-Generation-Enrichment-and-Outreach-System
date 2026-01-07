import time

def send_message(lead, messages, dry_run=True):
    time.sleep(0.5)
    if dry_run:
        return {"status": "DRY_RUN", "lead": lead["email"]}
    return {"status": "SENT"}