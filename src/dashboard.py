import json
import os

def generate_dashboard():
    log_file = "data/cost_log.json"
    
    # Load data
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            log = json.load(f)
    else:
        log = {"total_saved": 0, "total_runs": 0, "history": []}
    
    total_saved = log.get("total_saved", 0)
    total_runs = log.get("total_runs", 0)
    history = log.get("history", [])
    skip_count = sum(1 for h in history if h["decision"] == "skip")
    run_count = sum(1 for h in history if h["decision"] == "run")

    # Generate HTML
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>AutoSkip Dashboard</title>
    <style>
        body {{ font-family: Arial; background: #0d1117; color: #fff; padding: 30px; }}
        h1 {{ color: #58a6ff; }}
        .cards {{ display: flex; gap: 20px; margin: 20px 0; }}
        .card {{ background: #161b22; padding: 20px; border-radius: 10px; flex: 1; text-align: center; }}
        .card h2 {{ font-size: 40px; color: #3fb950; margin: 10px 0; }}
        .card p {{ color: #8b949e; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th {{ background: #161b22; padding: 10px; text-align: left; color: #58a6ff; }}
        td {{ padding: 10px; border-bottom: 1px solid #21262d; }}
        .skip {{ color: #f85149; }}
        .run {{ color: #3fb950; }}
    </style>
</head>
<body>
    <h1>🤖 AutoSkip Dashboard</h1>
    <div class="cards">
        <div class="card">
            <p>💰 Total Cost Saved</p>
            <h2>${total_saved:.2f}</h2>
        </div>
        <div class="card">
            <p>🚀 Pipelines Run</p>
            <h2>{total_runs}</h2>
        </div>
        <div class="card">
            <p>⏭️ Pipelines Skipped</p>
            <h2>{skip_count}</h2>
        </div>
    </div>
    <h2>📋 History</h2>
    <table>
        <tr><th>Time</th><th>Decision</th><th>Files Changed</th><th>Cost Saved</th></tr>
"""
    
    for h in reversed(history):
        decision_class = "skip" if h["decision"] == "skip" else "run"
        html += f"""
        <tr>
            <td>{h['timestamp']}</td>
            <td class="{decision_class}">{h['decision'].upper()}</td>
            <td>{', '.join(h['files_changed']) if isinstance(h['files_changed'], list) else h['files_changed']}</td>
            <td>${h['cost_saved']:.2f}</td>
        </tr>"""
    
    html += """
    </table>
</body>
</html>"""
    
    with open("dashboard.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print("✅ Dashboard generated: dashboard.html")

if __name__ == "__main__":
    generate_dashboard()