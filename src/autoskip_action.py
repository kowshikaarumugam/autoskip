# Security checks
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from security import verify_model_integrity, validate_input, log_audit, check_rate_limit

# Run security checks
if not check_rate_limit():
    sys.exit(1)

import subprocess
import pickle
import sys
import os
import json
from datetime import datetime

# Add src folder to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🔍 AutoSkip Analyzing commit...")

# Step 1 — Changed files
result = subprocess.run(
    ['git', 'diff', '--name-only', 'HEAD~1', 'HEAD'],
    capture_output=True, text=True
)
changed_files = result.stdout.strip().split('\n')
print(f"📁 Changed files: {changed_files}")

# Step 2 — File type analyze
code_extensions = ['.py', '.js', '.java', '.ts', '.yml', '.css', '.html']
has_code = 0
file_type_code = 0

for f in changed_files:
    ext = os.path.splitext(f)[1].lower()
    if ext in code_extensions:
        has_code = 1
        file_type_code = 1
        break

lines_changed = len(changed_files) * 10

# Step 3 — Model load
print("🧠 Loading AutoSkip model...")
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'model', 'autoskip_model.pkl')
with open(model_path, 'rb') as f:
    model = pickle.load(f)

# Step 4 — Predict
features = [[len(changed_files), file_type_code, lines_changed, has_code]]
prediction = model.predict(features)[0]
print(f"🤖 AutoSkip Decision: {prediction.upper()}")

# Step 5 — Cost tracking inline
COST_PER_RUN = 0.05
log_file = "data/cost_log.json"

if os.path.exists(log_file):
    with open(log_file, 'r') as f:
        log = json.load(f)
else:
    log = {"total_saved": 0, "total_runs": 0, "history": []}

entry = {
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "decision": prediction,
    "files_changed": changed_files,
    "cost_saved": COST_PER_RUN if prediction == "skip" else 0
}

if prediction == "skip":
    log["total_saved"] += COST_PER_RUN
else:
    log["total_runs"] += 1

log["history"].append(entry)

with open(log_file, 'w') as f:
    json.dump(log, f, indent=2)

print(f"💰 Total Saved: ${log['total_saved']:.2f}")
print(f"🚀 Total Runs: {log['total_runs']}")

# Step 6 — Decision
if prediction == 'skip':
    print("⏭️ PIPELINE SKIPPED — Only docs changed!")
else:
    print("✅ PIPELINE RUNNING — Code changes detected!")

sys.exit(0)
# Slack Notification
from notifier import send_slack_notification
send_slack_notification(prediction, changed_files, COST_PER_RUN if prediction == "skip" else 0)