import streamlit as st
import pandas as pd
from datetime import datetime
import os
import ramai_engine as ramai  # Importing your modular brain

st.set_page_config(page_title="PondGuard AI", layout="wide")

st.title("🛡️ PondGuard Intelligence Dashboard")
st.caption("Powered by RAMAI AI | Bhimavaram - Rajahmundry Hub")

# Sidebar
st.sidebar.header("📡 Sensor Inputs")
temp = st.sidebar.slider("Temp", 20.0, 40.0, 28.0)
ph = st.sidebar.slider("pH", 0.0, 14.0, 7.5)
do = st.sidebar.slider("Oxygen", 0.0, 10.0, 6.0)

# Dashboard Columns
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🤖 RAMAI Analysis")
    status, en_msg, te_msg, color = ramai.get_ramai_advice(temp, ph, do)
    
    if color == "red": st.error(f"{status}: {te_msg}")
    elif color == "orange": st.warning(f"{status}: {te_msg}")
    else: st.success(f"{status}: {te_msg}")
    
    if st.button("📢 Play Voice Alert"):
        ramai.play_voice(te_msg)

with col2:
    st.subheader("📊 Data Management")
    if st.button("💾 Record Data to D: Drive"):
        file_path = "D:/PondGuard_Project/pond_history.csv"
        df = pd.DataFrame({"Timestamp": [datetime.now()], "Temp": [temp], "pH": [ph], "Oxygen": [do]})
        df.to_csv(file_path, mode='a', index=False, header=not os.path.isfile(file_path))
        st.toast("Data Logged!")

# Show Graph
if os.path.isfile("D:/PondGuard_Project/pond_history.csv"):
    st.divider()
    history = pd.read_csv("D:/PondGuard_Project/pond_history.csv")
    st.line_chart(history.set_index("Timestamp")[["Oxygen", "pH"]])