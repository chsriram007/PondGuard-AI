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

file_path = "D:/PondGuard_Project/data/pond_history.csv"

with col2:
    st.subheader("📊 Data Logging")
    if st.button("💾 Save to Cloud (D: Drive)"):
        # We use the path defined above
        df = pd.DataFrame({
            "Timestamp": [datetime.now()],
            "Farmer_ID": [farmer_id],
            "Location": [pond_location],
            "Temp": [temp], "pH": [ph], "Oxygen": [do]
        })
        df.to_csv(file_path, mode='a', index=False, header=not os.path.isfile(file_path))
        st.toast(f"Data saved for {farmer_id}!")

# --- SEARCH & FILTER SECTION ---
# --- SEARCH & FILTER SECTION ---
st.divider()
st.header("🔍 Filtered History")

if os.path.isfile(file_path):
    # We load the file and call it 'all_data'
    all_data = pd.read_csv(file_path)
    
    # We must use 'all_data' here, not 'df'
    unique_farmers = all_data['Farmer_ID'].unique() 
    selected_farmer = st.selectbox("Select Farmer to track:", unique_farmers)
    
    # Filter the data
    filtered_df = all_data[all_data['Farmer_ID'] == selected_farmer]
    
    st.write(f"Displaying history for: {selected_farmer}")
    st.dataframe(filtered_df)
    
    # Show the chart for the filtered data
    st.line_chart(filtered_df.set_index("Timestamp")[["Oxygen"]])

import io  # Add this at the top of your app.py with other imports

# ... (inside your Search & Filter section, after the line_chart) ...

# Create a buffer to hold the Excel data in memory
buffer = io.BytesIO()

# Use Pandas to write the filtered data to the buffer
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    filtered_df.to_excel(writer, index=False, sheet_name='PondHistory')
    
# Create the Download Button
st.download_button(
    label=f"📥 Download {selected_farmer} Report (Excel)",
    data=buffer.getvalue(),
    file_name=f"PondGuard_{selected_farmer}_{datetime.now().strftime('%Y%m%d')}.xlsx",
    mime="application/vnd.ms-excel"
)