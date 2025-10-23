import streamlit as st
import psutil
import pandas as pd
import time
from datetime import datetime

st.set_page_config(page_title="System Metrics Dashboard", layout="wide")
 
st.title("Real-Time System Metrics Dashboard")

# Initialize session state to store time-series data
if 'metrics_data' not in st.session_state:
    st.session_state.metrics_data = pd.DataFrame(columns=["timestamp", "cpu", "memory", "disk"])
    
# Function to collect system metrics

def get_metrics():    
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    timestamp = datetime.now().strftime('%H:%M:%S')
    return {"timestamp": timestamp, "cpu": cpu, "memory": memory, "disk": disk}

# Layout columns
col1, col2, col3 = st.columns(3)
 
# Auto-refresh every 5 seconds
placeholder = st.empty()     

while True:
    metric = get_metrics()
    st.session_state.metrics_data = pd.concat([st.session_state.metrics_data, pd.DataFrame([metric])],ignore_index=True).tail(30)  # keep last 30 entries
    # Gauge-like metrics
    col1.metric("CPU Usage (%)", f"{metric['cpu']}%")
    col2.metric("Memory Usage (%)", f"{metric['memory']}%")
    col3.metric("Disk Usage (%)", f"{metric['disk']}%")
    with placeholder.container():
        st.subheader("Time Series: Metrics Over Time")
        st.line_chart(st.session_state.metrics_data.set_index("timestamp"))
 
    time.sleep(5)