import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="AutoSkip Dashboard",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AutoSkip — AI-Powered CI/CD Optimizer")
st.markdown("**Real-time pipeline decision tracker**")

# Load data
log_file = "data/cost_log.json"

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

# Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Saved", f"${total_saved:.2f}")
col2.metric("🚀 Pipelines Run", total_runs)
col3.metric("⏭️ Pipelines Skipped", skip_count)
col4.metric("📊 Total Commits", len(history))

st.divider()

# Chart
if len(history) > 0:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Skip vs Run")
        chart_data = pd.DataFrame({
            "Decision": ["Skip", "Run"],
            "Count": [skip_count, run_count]
        })
        fig = px.pie(chart_data, values="Count", names="Decision",
                    color_discrete_map={"Skip": "#f85149", "Run": "#3fb950"})
        st.plotly_chart(fig)
    
    with col2:
        st.subheader("Cost Savings Over Time")
        df = pd.DataFrame(history)
        df["cumulative_saved"] = df["cost_saved"].cumsum()
        fig2 = px.line(df, x="timestamp", y="cumulative_saved",
                      labels={"cumulative_saved": "Total Saved ($)"},
                      color_discrete_sequence=["#58a6ff"])
        st.plotly_chart(fig2)

    st.divider()
    
    # History table
    st.subheader("📋 Commit History")
    df_display = pd.DataFrame(history)[["timestamp", "decision", "cost_saved"]]
    df_display.columns = ["Time", "Decision", "Cost Saved ($)"]
    st.dataframe(df_display, use_container_width=True)

else:
    st.info("No pipeline runs yet! Push some code to see data here.")

# Auto refresh
st.button("🔄 Refresh")