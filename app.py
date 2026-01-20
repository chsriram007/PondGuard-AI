import streamlit as st
import pandas as pd
from datetime import datetime
import os
import src.ramai_engine as ramai 

st.set_page_config(page_title="PondGuard AI", layout="wide")

# --- SIDEBAR: FARMER REGISTRATION ---
st.sidebar.header("👤 Farmer Profile")
farmer_id = st.sidebar.text_input("Enter Farmer ID", "FG-001")
pond_location = st.sidebar.selectbox("Pond Location", ["Bhimavaram", "Rajahmundry", "Other"])

# --- MAIN UI ---
st.title(f"🛡️ PondGuard: {farmer_id}")
st.caption(f"Active Monitoring at {pond_location}")

# Sensor Sliders
temp = st.sidebar.slider("Temp", 20.0, 40.0, 28.0)
ph = st.sidebar.slider("pH", 0.0, 14.0, 7.5)
do = st.sidebar.slider("Oxygen", 0.0, 10.0, 6.0)

col1, col2 = st.columns(2)

with col1:
    st.subheader("🤖 RAMAI Advice")
    status, en_msg, te_msg, color = ramai.get_ramai_advice(temp, ph, do)
    
    # Display Alert
    if color == "red": st.error(te_msg)
    else: st.success(te_msg)
    
    if st.button("📢 Voice Alert"):
        ramai.play_voice(te_msg)

with col2:
    st.subheader("📊 Data Logging")
    if st.button("💾 Save to Cloud (D: Drive)"):
        # We now save the Farmer ID and Location so we can filter data later
        file_path = "D:/PondGuard_Project/data/pond_history.csv"
        df = pd.DataFrame({
            "Timestamp": [datetime.now()],
            "Farmer_ID": [farmer_id],
            "Location": [pond_location],
            "Temp": [temp], "pH": [ph], "Oxygen": [do]
        })
        df.to_csv(file_path, mode='a', index=False, header=not os.path.isfile(file_path))
        st.toast(f"Data saved for {farmer_id}!")