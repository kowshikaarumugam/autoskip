import hashlib
import os
import json
from datetime import datetime

# ✅ 1. Model Integrity Check
def verify_model_integrity(model_path):
    if not os.path.exists(model_path):
        print("❌ Model file missing!")
        return False
    
    with open(model_path, 'rb') as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    
    hash_file = model_path + ".hash"
    
    if os.path.exists(hash_file):
        with open(hash_file, 'r') as f:
            saved_hash = f.read().strip()
        
        if file_hash != saved_hash:
            print("❌ SECURITY ALERT: Model file tampered!")
            return False
        else:
            print("✅ Model integrity verified!")
            return True
    else:
        # First time — save hash
        with open(hash_file, 'w') as f:
            f.write(file_hash)
        print("✅ Model hash saved!")
        return True

# ✅ 2. Input Validation
def validate_input(changed_files):
    if not changed_files or changed_files == ['']:
        print("⚠️ No files changed!")
        return False
    
    # Malicious path check
    for f in changed_files:
        if '..' in f or f.startswith('/'):
            print(f"❌ SECURITY ALERT: Suspicious path detected: {f}")
            return False
    
    print("✅ Input validation passed!")
    return True

# ✅ 3. Audit Log
def log_audit(decision, changed_files, user="github-actions"):
    audit_file = "data/audit_log.json"
    
    if os.path.exists(audit_file):
        with open(audit_file, 'r') as f:
            audit = json.load(f)
    else:
        audit = {"logs": []}
    
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": user,
        "decision": decision,
        "files": changed_files,
        "ip": "github-actions-runner"
    }
    
    audit["logs"].append(entry)
    
    with open(audit_file, 'w') as f:
        json.dump(audit, f, indent=2)
    
    print(f"✅ Audit log updated!")

# ✅ 4. Rate Limiting
def check_rate_limit(max_runs=10):
    rate_file = "data/rate_limit.json"
    today = datetime.now().strftime("%Y-%m-%d")
    
    if os.path.exists(rate_file):
        with open(rate_file, 'r') as f:
            rate = json.load(f)
    else:
        rate = {"date": today, "count": 0}
    
    if rate["date"] != today:
        rate = {"date": today, "count": 0}
    
    if rate["count"] >= max_runs:
        print(f"❌ Rate limit exceeded! Max {max_runs} runs per day!")
        return False
    
    rate["count"] += 1
    
    with open(rate_file, 'w') as f:
        json.dump(rate, f, indent=2)
    
    print(f"✅ Rate limit OK ({rate['count']}/{max_runs})")
    return True