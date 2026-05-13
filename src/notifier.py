import requests
import os
import json

def send_slack_notification(decision, changed_files, cost_saved=0):
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    
    if not webhook_url:
        print("⚠️ Slack webhook URL not found!")
        return
    
    if decision == "skip":
        emoji = "⏭️"
        color = "#f85149"
        title = "Pipeline SKIPPED"
        message = f"Only docs changed — pipeline skipped!\nFiles: {', '.join(changed_files)}\nCost Saved: ${cost_saved:.2f}"
    else:
        emoji = "✅"
        color = "#3fb950"
        title = "Pipeline RUNNING"
        message = f"Code changes detected — pipeline running!\nFiles: {', '.join(changed_files)}"
    
    payload = {
        "attachments": [
            {
                "color": color,
                "title": f"{emoji} AutoSkip — {title}",
                "text": message,
                "footer": "AutoSkip Bot"
            }
        ]
    }
    
    response = requests.post(
        webhook_url,
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        print("✅ Slack notification sent!")
    else:
        print(f"❌ Slack notification failed: {response.status_code}")