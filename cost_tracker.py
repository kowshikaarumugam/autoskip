import json
import os
from datetime import datetime

# Average CI/CD run cost
COST_PER_RUN = 0.05  # $0.05 per pipeline run

def save_cost(decision, files_changed):
    log_file = "data/cost_log.json"
    
    # Load existing log
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            log = json.load(f)
    else:
        log = {"total_saved": 0, "total_runs": 0, "history": []}
    
    # Update log
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "decision": decision,
        "files_changed": files_changed,
        "cost_saved": COST_PER_RUN if decision == "skip" else 0
    }
    
    if decision == "skip":
        log["total_saved"] += COST_PER_RUN
    else:
        log["total_runs"] += 1
    
    log["history"].append(entry)
    
    # Save log
    with open(log_file, 'w') as f:
        json.dump(log, f, indent=2)
    
    print(f"💰 Total Saved So Far: ${log['total_saved']:.2f}")
    print(f"🚀 Total Runs: {log['total_runs']}")
    return log