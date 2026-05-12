import subprocess
import pickle
import sys
import os

print("🔍 AutoSkip Analyzing commit...")

# Step 1 — Changed files get பண்றோம்
result = subprocess.run(
    ['git', 'diff', '--name-only', 'HEAD~1', 'HEAD'],
    capture_output=True, text=True
)
changed_files = result.stdout.strip().split('\n')
print(f"📁 Changed files: {changed_files}")

# Step 2 — File type analyze பண்றோம்
code_extensions = ['.py', '.js', '.java', '.ts', '.yml', '.css', '.html']
doc_extensions = ['.md', '.txt', '.csv']

has_code = 0
file_type_code = 0

for f in changed_files:
    ext = os.path.splitext(f)[1].lower()
    if ext in code_extensions:
        has_code = 1
        file_type_code = 1
        break
    elif ext in doc_extensions:
        file_type_code = 0

lines_changed = len(changed_files) * 10

# Step 3 — Model load பண்றோம்
print("🧠 Loading AutoSkip model...")
with open('model/autoskip_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Step 4 — Predict பண்றோம்
features = [[len(changed_files), file_type_code, lines_changed, has_code]]
prediction = model.predict(features)[0]

print(f"🤖 AutoSkip Decision: {prediction.upper()}")

# Step 5 — Decision
if prediction == 'skip':
    print("⏭️ PIPELINE SKIPPED — Only docs changed!")
    from cost_tracker import save_cost
    save_cost("skip", changed_files)
    sys.exit(0)
else:
    print("✅ PIPELINE RUNNING — Code changes detected!")
    from cost_tracker import save_cost
    save_cost("run", changed_files)
    sys.exit(0)