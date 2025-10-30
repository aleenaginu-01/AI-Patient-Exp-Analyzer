import streamlit as st
import requests
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
import time
from datetime import datetime, date
import os
from collections import Counter
from dotenv import load_dotenv

load_dotenv(override=True)
API_URL = os.getenv("API_URL")
CALL_API_URL=os.getenv("CALL_API_URL")



def calculate_duration(start_iso: str, end_iso: str) -> str:
    """Calculates duration between two ISO 8601 timestamps."""
    try:
        # Handle 'Z' for UTC
        start = datetime.fromisoformat(start_iso.replace('Z', '+00:00'))
        end = datetime.fromisoformat(end_iso.replace('Z', '+00:00'))
        duration_sec = (end - start).total_seconds()

        minutes = int(duration_sec // 60)
        seconds = int(duration_sec % 60)

        return f"{minutes} min, {seconds} sec"
    except Exception as e:
        print(f"Error calculating duration: {e}")
        return "N/A"

def get_sentiment_emoji(sentiment: str) -> str:
    """Returns an emoji for the sentiment string."""
    if sentiment == "POSITIVE":
        return "✅"
    if sentiment == "ALERT":
        return "🚩" # Red flag for alerts
    if sentiment == "NEGATIVE":
        return "❌" # Should be rare, as it's covered by ALERT
    return "➖"

def get_adherence_emoji(adherence: str) -> str:
    """Returns an emoji for the adherence classification."""
    if adherence == "ADHERENT":
        return "✅" # Checkmark
    if adherence == "NON-ADHERENT":
        return "⚠️" # Warning sign
    return "❓" # Question mark for Unclear
# --- END HELPER ---

# --- (2) NEW HELPER FOR SIDE EFFECTS EMOJI ---
def get_side_effects_display(reported: bool) -> str:
    """Returns an emoji and text for side effects status."""
    if reported:
        return "❗ Reported" # Exclamation for reported
    return "➖ None Reported"

st.set_page_config(page_title="Admin Dashboard", layout="wide")

# Enhanced CSS with professional styling
hide_default_format = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

        * {
            font-family: 'Poppins', sans-serif;
        }

        /* Hide Streamlit branding */
        header[data-testid="stHeader"] {display: none;}
        [data-testid="stSidebarNav"] {display: none;}
        [data-testid="stSidebarNavItems"] {display: none;}
        [data-testid="stToolbar"] {display: none;}
        footer {display: none;}

        /* Main App Background */
        .stApp {
            background: linear-gradient(135deg, #0a1e2b 0%, #0f2027 50%, #203a43 100%);
            color: #e8f5f7;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0d1b2a 0%, #1b263b 100%);
            border-right: 2px solid #14b8a6;
        }

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: #a7f3d0;
        }

        /* Sidebar Header */
        [data-testid="stSidebar"] h1 {
            color: #14b8a6 !important;
            font-size: 28px !important;
            font-weight: 700 !important;
            text-align: center;
            padding: 20px 0;
            background: linear-gradient(135deg, #14b8a6 0%, #06b6d4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: glow 2s ease-in-out infinite;
        }

        /* Sidebar Radio Buttons */
        [data-testid="stSidebar"] .stRadio > label {
            color: #14b8a6 !important;
            font-weight: 600 !important;
            font-size: 16px !important;
            margin-bottom: 15px !important;
        }

        [data-testid="stSidebar"] .stRadio > div {
            gap: 8px;
        }

        [data-testid="stSidebar"] .stRadio label {
            background: rgba(20, 184, 166, 0.1);
            padding: 14px 20px;
            border-radius: 10px;
            transition: all 0.3s ease;
            border: 1px solid transparent;
            color: #a7f3d0 !important;
            font-size: 15px !important;
            display: block;
            width: 100%;
        }

        [data-testid="stSidebar"] .stRadio label:hover {
            background: rgba(20, 184, 166, 0.2);
            border: 1px solid #14b8a6;
            transform: translateX(5px);
        }

        /* Main Header */
        h1, h2, h3 {
            color: #14b8a6 !important;
            font-weight: 600 !important;
        }

        h1 {
            font-size: 42px !important;
            text-align: center;
            margin-bottom: 10px !important;
            text-shadow: 0 0 20px rgba(20, 184, 166, 0.3);
            animation: fadeInDown 0.8s ease;
        }

        h2 {
            font-size: 28px !important;
            margin-top: 30px !important;
        }

        h3 {
            font-size: 22px !important;
        }

        /* Subheader styling */
        .stMarkdownContainer h3 {
            background: linear-gradient(135deg, #14b8a6 0%, #06b6d4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 600;
        }

        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #14b8a6 0%, #06b6d4 100%);
            color: white !important;
            border: none;
            border-radius: 10px;
            padding: 12px 28px;
            font-weight: 600;
            font-size: 15px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(20, 184, 166, 0.3);
        }

        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 25px rgba(20, 184, 166, 0.5);
            background: linear-gradient(135deg, #06b6d4 0%, #14b8a6 100%);
        }

        # In your dashboard.py hide_default_format CSS, replace the Input Fields section with:

        /* Input Fields */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stTextArea textarea {
            background: rgba(20, 184, 166, 0.05) !important;
            border: 1px solid #14b8a6 !important;
            border-radius: 8px !important;
            color: #e8f5f7 !important;
            padding: 10px !important;
        }

        /* Selectbox Container */
        .stSelectbox {
            color: #e8f5f7 !important;
        }

        /* Selectbox Input Wrapper */
        .stSelectbox > div > div {
            background: rgba(20, 184, 166, 0.05) !important;
            border: 1px solid #14b8a6 !important;
            border-radius: 8px !important;
        }

        /* Selectbox - the actual select element */
        .stSelectbox select {
            background: rgba(20, 184, 166, 0.05) !important;
            color: #e8f5f7 !important;
            border: none !important;
        }

        /* Selectbox - BaseWeb Select component */
        .stSelectbox div[data-baseweb="select"] {
            background: rgba(20, 184, 166, 0.05) !important;
        }

        /* Selectbox - Selected value container */
        .stSelectbox div[data-baseweb="select"] > div {
            background: rgba(20, 184, 166, 0.05) !important;
            border: 1px solid #14b8a6 !important;
            border-radius: 8px !important;
        }

        /* Selectbox - Selected value text */
        .stSelectbox div[data-baseweb="select"] > div > div {
            color: #e8f5f7 !important;
        }

        /* Selectbox - All text inside */
        .stSelectbox * {
            color: #e8f5f7 !important;
        }

        /* Selectbox dropdown menu */
        div[data-baseweb="popover"] {
            background: #1b263b !important;
        }

        /* Selectbox dropdown list */
        ul[role="listbox"] {
            background: #1b263b !important;
            border: 1px solid #14b8a6 !important;
        }

        /* Selectbox dropdown options */
        li[role="option"] {
            background: #1b263b !important;
            color: #e8f5f7 !important;
        }

        /* Selectbox dropdown options hover */
        li[role="option"]:hover {
            background: rgba(20, 184, 166, 0.2) !important;
            color: #14b8a6 !important;
        }

        /* Selectbox dropdown selected option */
        li[role="option"][aria-selected="true"] {
            background: rgba(20, 184, 166, 0.3) !important;
            color: #14b8a6 !important;
        }

        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus,
        .stSelectbox > div > div:focus-within,
        .stTextArea textarea:focus {
            border: 2px solid #06b6d4 !important;
            box-shadow: 0 0 10px rgba(20, 184, 166, 0.3) !important;
        }

        /* Date Input Styling */
        .stDateInput > div > div {
            background: rgba(20, 184, 166, 0.05) !important;
            border: 1px solid #14b8a6 !important;
            border-radius: 8px !important;
        }

        .stDateInput input {
            background: rgba(20, 184, 166, 0.05) !important;
            color: #e8f5f7 !important;
            border: none !important;
        }

        /* Date picker calendar styling */
        .stDateInput div[data-baseweb="calendar"] {
            background: #1b263b !important;
            border: 1px solid #14b8a6 !important;
        }

        /* Calendar dates */
        .stDateInput button {
            color: #e8f5f7 !important;
        }

        /* Calendar selected date */
        .stDateInput button[aria-selected="true"] {
            background: #14b8a6 !important;
            color: white !important;
        }

        /* Calendar hover */
        .stDateInput button:hover {
            background: rgba(20, 184, 166, 0.2) !important;
        }
        /* Labels */
        .stTextInput > label,
        .stNumberInput > label,
        .stSelectbox > label,
        .stDateInput > label,
        .stTextArea > label {
            color: #a7f3d0 !important;
            font-weight: 500 !important;
            font-size: 15px !important;
        }

        /* Cards & Containers */
        .stContainer {
            background: rgba(20, 184, 166, 0.05);
            border: 1px solid rgba(20, 184, 166, 0.2);
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
            transition: all 0.3s ease;
            animation: fadeIn 0.5s ease;
        }

        .stContainer:hover {
            border-color: #14b8a6;
            box-shadow: 0 5px 20px rgba(20, 184, 166, 0.2);
        }

        /* DataFrames */
        .stDataFrame {
            border: 1px solid #14b8a6;
            border-radius: 10px;
            overflow: hidden;
        }

        /* Success/Error/Warning Messages */
        .stSuccess {
            background: rgba(20, 184, 166, 0.1) !important;
            border-left: 4px solid #14b8a6 !important;
            color: #a7f3d0 !important;
        }

        .stError {
            background: rgba(239, 68, 68, 0.1) !important;
            border-left: 4px solid #ef4444 !important;
        }

        .stWarning {
            background: rgba(251, 191, 36, 0.1) !important;
            border-left: 4px solid #fbbf24 !important;
        }

        .stInfo {
            background: rgba(6, 182, 212, 0.1) !important;
            border-left: 4px solid #06b6d4 !important;
            color: #a7f3d0 !important;
        }

        /* Divider */
        hr {
            border: none;
            height: 2px;
            background: linear-gradient(90deg, transparent, #14b8a6, transparent);
            margin: 30px 0;
        }

        /* File Uploader */
        [data-testid="stFileUploader"] {
            background: rgba(20, 184, 166, 0.05);
            border: 2px dashed #14b8a6;
            border-radius: 10px;
            padding: 20px;
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }

        .stTabs [data-baseweb="tab"] {
            background: rgba(20, 184, 166, 0.1);
            border-radius: 8px;
            color: #a7f3d0;
            padding: 10px 20px;
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #14b8a6 0%, #06b6d4 100%);
            color: white;
        }

        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes glow {
            0%, 100% { text-shadow: 0 0 10px rgba(20, 184, 166, 0.5); }
            50% { text-shadow: 0 0 20px rgba(20, 184, 166, 0.8); }
        }

        /* Custom metric cards */
        .metric-card {
            background: linear-gradient(135deg, rgba(20, 184, 166, 0.1) 0%, rgba(6, 182, 212, 0.1) 100%);
            border: 1px solid rgba(20, 184, 166, 0.3);
            color: #e8f5f7;
            text-align: center;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
            margin: 10px;
            animation: fadeIn 0.6s ease;
        }

        .metric-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 8px 25px rgba(20, 184, 166, 0.4);
            border-color: #14b8a6;
        }

        .metric-label {
            font-size: 16px;
            font-weight: 500;
            margin-top: 15px;
            color: #a7f3d0;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .metric-value {
            font-size: 36px;
            font-weight: 700;
            color: #14b8a6;
            text-shadow: 0 0 10px rgba(20, 184, 166, 0.3);
        }

        /* Chat box styling */
        .chat-box {
            background: linear-gradient(135deg, #0d1b2a 0%, #1b263b 100%);
            border: 1px solid #14b8a6;
            border-radius: 15px;
            padding: 20px;
            height: 400px;
            overflow-y: auto;
            font-family: 'Poppins', sans-serif;
            font-size: 15px;
            color: #e8f5f7;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
        }

        .message {
            margin: 12px 0;
            padding: 12px 18px;
            border-radius: 12px;
            width: fit-content;
            max-width: 75%;
            animation: fadeIn 0.4s ease;
        }

        .ai {
            background: linear-gradient(135deg, rgba(20, 184, 166, 0.2) 0%, rgba(6, 182, 212, 0.2) 100%);
            color: #a7f3d0;
            text-align: left;
            border-left: 3px solid #14b8a6;
        }

        .user {
            background: linear-gradient(135deg, rgba(167, 243, 208, 0.1) 0%, rgba(20, 184, 166, 0.1) 100%);
            color: #e8f5f7;
            text-align: right;
            margin-left: auto;
            border-right: 3px solid #06b6d4;
        }

        /* Vision/Mission cards */
        .vision-card {
            background: linear-gradient(135deg, rgba(20, 184, 166, 0.1) 0%, rgba(6, 182, 212, 0.05) 100%);
            padding: 30px;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(20, 184, 166, 0.3);
            transition: all 0.4s ease;
            animation: fadeIn 0.8s ease;
        }

        .vision-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 12px 35px rgba(20, 184, 166, 0.4);
            border-color: #14b8a6;
        }

        .vision-card h4 {
            color: #14b8a6 !important;
            font-size: 22px !important;
            font-weight: 600 !important;
            margin: 15px 0 !important;
        }

        .vision-card p {
            color: #a7f3d0 !important;
            font-size: 15px !important;
            line-height: 1.6 !important;
        }

        /* Compact buttons for patient list */
        .compact-btn {
            padding: 6px 12px !important;
            font-size: 13px !important;
            min-height: 35px !important;
            height: 35px !important;
        }

        /* Patient list row styling */
        .patient-row {
            padding: 8px 0 !important;
            margin: 5px 0 !important;
        }
    </style>
"""
st.markdown(hide_default_format, unsafe_allow_html=True)

st.header("🏥 CareLoop.AI")
st.sidebar.header("CareLoop.AI")
st.sidebar.title("Admin Panel")

menu = st.sidebar.radio(
    "Select View:",
    ["Dashboard", "Add Patients", "Patient List", "Start Patient Follow-Up", "Patient Feedback","Analytics","Appointments", "Logout"],
    label_visibility="visible",
)

st.sidebar.divider()

if menu == "Add Patients":
    st.subheader("📂 Upload or Add Patients")
    uploaded_file = st.file_uploader("Upload your CSV file", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("Patient data uploaded successfully!")
        st.dataframe(df)

        if st.button("Add Uploaded Data to Database"):
            success_count = 0
            fail_count = 0

            for _, row in df.iterrows():
                prescribed_medication = []
                if "prescribed_medication" in df.columns:
                    meds = row.get("prescribed_medication", "")
                    prescribed_medication = [m.strip() for m in str(meds).split(",") if m.strip()]

                patient_data = {
                    "name": row.get("name", ""),
                    "age": int(row.get("age", 0)),
                    "gender": row.get("gender", ""),
                    "phone": str(row.get("phone", "")),
                    "disease": row.get("disease", ""),
                    "visit_date": str(row.get("visit_date", "")),
                    "prescribed_medication": prescribed_medication,
                    "next_visit_date": str(row.get("next_visit_date", "")),
                }

                try:
                    response = requests.post(API_URL + "/patient", json=patient_data)
                    if response.status_code in (200, 201):
                        success_count += 1
                    else:
                        fail_count += 1
                except Exception as e:
                    fail_count += 1
                    print("Error:", e)

            st.success(f"✅ {success_count} patients added successfully!")
            if fail_count:
                st.warning(f"⚠️ {fail_count} records failed to upload. Check formatting or API connection.")

    st.subheader("Add Patients Details")
    with st.form("add_patient_form"):
        name = st.text_input("Patient Name")
        age = st.number_input("Age", min_value=0, max_value=120)
        gender = st.selectbox("Gender", ["Male", "Female"], index=0)
        phone = st.text_input("Phone Number")
        disease = st.text_input("Disease / Condition")
        # visit_date = st.text_input("Visit Date")
        visit_date = st.date_input("Visit Date", value=date.today())
        pre_medi = st.text_input("Prescribed Medication")
        # next_visit_date = st.text_input("Next Visit Date")
        next_visit_date = st.date_input("Next Visit Datee", value=date.today())
        submitted = st.form_submit_button("Add Patient")
        if submitted:
            prescribed_medication = [pm.strip() for pm in pre_medi.split(",") if pm.strip()]
            patient_data = {
                "name": name,
                "age": age,
                "gender": gender,
                "phone": phone,
                "disease": disease,
                "visit_date": str(visit_date),
                "prescribed_medication": prescribed_medication,
                "next_visit_date": str(next_visit_date),
            }
            response = requests.post(API_URL + "/patient", json=patient_data)
            if response.status_code in (200, 201):
                st.success(f"Patient {name} added successfully!")
            else:
                st.error(f"Error adding patient {response.text}")

elif menu == "Dashboard":
    st.title("Admin Dashboard")
    # st.write("Welcome, Admin! 👩‍⚕️")
    total_patients = "N/A"
    total_engaged = "N/A"
    total_alerts = "N/A"
    alert_delta_text = None
    alert_delta_color = "normal"

    # --- Fetch Metrics ---
    try:
        # Get total patients count
        patients_res = requests.get(f"{API_URL}/patient")
        if patients_res.status_code == 200:
            total_patients = len(patients_res.json())
        else:
            st.warning("Could not fetch total patient count.")

        # Get engagement and alert metrics
        metrics_res = requests.get(f"{API_URL}/patient/metrics")
        if metrics_res.status_code == 200:
            metrics_data = metrics_res.json()
            total_engaged = metrics_data.get('total_patients_engaged', 0)
            total_alerts = metrics_data.get('total_flagged_alerts', 0)
            if total_alerts > 0:
                alert_delta_text = f"{total_alerts} High Priority"
                alert_delta_color = "inverse"  # Makes delta red
        else:
            st.warning("Could not fetch dashboard metrics.")

    except Exception as e:
        st.error(f"Error connecting to API: {e}")
    # --- End Fetch Metrics ---

    st.subheader("📊 Key Metrics")  # Changed subheader
    # st.write("Visual insights and performance overview") # Optional text

    # --- Display Dynamic Metric Cards ---
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
                <div class="metric-card">
                    <img src="https://cdn-icons-png.flaticon.com/512/4320/4320371.png" width="60">
                    <div class="metric-label">Total Patients</div>
                    <div class="metric-value">{total_patients}</div>
                </div>
                """, unsafe_allow_html=True)
    with col2:
        # Using a phone/call icon for engaged
        st.markdown(
            f"""
                <div class="metric-card">
                    <img src="https://cdn-icons-png.flaticon.com/512/455/455705.png" width="60">
                    <div class="metric-label">Patients Engaged</div>
                    <div class="metric-value">{total_engaged}</div>
                </div>
                """, unsafe_allow_html=True)

    with col3:
        # Using the existing alert icon
        st.markdown(
            f"""
                <div class="metric-card">
                    <img src="https://cdn-icons-png.flaticon.com/512/7249/7249210.png" width="60">
                    <div class="metric-label">Active Alerts</div>
                    <div class="metric-value">{total_alerts}</div>
                </div>
                """, unsafe_allow_html=True)
        # Optionally add the delta text below the card if needed,
        # st.metric doesn't integrate well with custom HTML cards
        # if alert_delta_text:
        #     st.markdown(f"<p style='text-align:center; color: #ef4444;'>{alert_delta_text}</p>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<h3 style="color: #14b8a6; margin-top: 40px;">📈 Insights Overview</h3>', unsafe_allow_html=True)
    col_left, col_right = st.columns(2)

    call_records = []
    try:
        records_res = requests.get(f"{API_URL}/patient/call-records")
        if records_res.status_code == 200:
            call_records = records_res.json()
        else:
            st.warning("Could not fetch call records for charts.")
    except Exception as e:
        st.error(f"Error connecting to API for call records: {e}")

    # --- Generate Charts ---
    col_left, col_right = st.columns(2)

    # 1. Sentiment Pie Chart
    with col_left:
        st.subheader("Follow-up Sentiment")
        fig1, ax1 = plt.subplots(facecolor='#0a1e2b')  # Keep background styling
        ax1.set_facecolor('#0a1e2b')

        if call_records:
            sentiments = [record.get('overall_sentiment', 'NEUTRAL') for record in call_records]
            sentiment_counts = Counter(sentiments)

            # Ensure order and presence of all categories
            labels = ["POSITIVE", "NEUTRAL", "ALERT"]
            sizes = [sentiment_counts.get(label, 0) for label in labels]
            colors = ['#06b6d4', '#a7f3d0', '#044954']

            # Filter out zero-value slices to avoid display issues
            non_zero_labels = [label for i, label in enumerate(labels) if sizes[i] > 0]
            non_zero_sizes = [size for size in sizes if size > 0]
            non_zero_colors = [color for i, color in enumerate(colors) if sizes[i] > 0]

            if non_zero_sizes:  # Only plot if there's data
                ax1.pie(non_zero_sizes, labels=non_zero_labels, autopct='%1.1f%%', startangle=90,
                        colors=non_zero_colors,
                        textprops={'color': '#e8f5f7', 'fontsize': 12, 'weight': 'bold'})
                ax1.axis('equal')
            else:
                ax1.text(0.5, 0.5, 'No Sentiment Data', horizontalalignment='center', verticalalignment='center',
                         color='#e8f5f7')
                ax1.axis('off')  # Hide axes if no data
        else:
            ax1.text(0.5, 0.5, 'No Call Records Found', horizontalalignment='center', verticalalignment='center',
                     color='#e8f5f7')
            ax1.axis('off')  # Hide axes if no data

        st.pyplot(fig1)

    # 2. Adherence Bar Chart
    with col_right:
        st.subheader("Medication Adherence")
        fig2, ax2 = plt.subplots(facecolor='#0a1e2b')
        ax2.set_facecolor('#0a1e2b')

        if call_records:
            # Get the CLASSIFIED adherence status directly
            adherence_statuses_raw = [
                record.get('medical_adherence', 'NOT_ASKED') # Default to UNCLEAR if missing
                for record in call_records
            ]
            adherence_statuses = [
                "UNCLEAR" if status == "NOT_ASKED" else status
                for status in adherence_statuses_raw
            ]
            adherence_counts = Counter(adherence_statuses)

            # Define categories based on the classification output
            categories = ["ADHERENT", "NON-ADHERENT", "UNCLEAR"]
            values = [adherence_counts.get(cat, 0) for cat in categories]
            bar_colors = ["#14b8a6", "#044954", "#a7f3d0"]

            if any(v > 0 for v in values): # Only plot if there's data
                bars = ax2.bar(categories, values, color=bar_colors)
                ax2.set_ylabel("Number of Patients", color='#e8f5f7', fontweight='bold')
                ax2.tick_params(axis='x', colors='#e8f5f7')
                ax2.tick_params(axis='y', colors='#e8f5f7')
                ax2.spines['bottom'].set_color('#14b8a6')
                ax2.spines['left'].set_color('#14b8a6')
                ax2.spines['top'].set_visible(False)
                ax2.spines['right'].set_visible(False)
                ax2.bar_label(bars, color='#e8f5f7', padding=3) # Add counts on top
            else:
                ax2.text(0.5, 0.5, 'No Adherence Data',transform=ax2.transAxes, # Use axes coordinates
                         horizontalalignment='center',
                         verticalalignment='center',
                         color='#e8f5f7')
                ax2.axis('off')
        else:
             ax2.text(0.5, 0.5, 'No Call Records Found',transform=ax2.transAxes, # Use axes coordinates
                         horizontalalignment='center',
                         verticalalignment='center',
                         color='#e8f5f7')
             ax2.axis('off')

        st.pyplot(fig2)


    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
            <div class='vision-card'>
                <img src='https://cdn-icons-png.flaticon.com/512/3176/3176367.png' width='80'>
                <h4>Our Vision</h4>
                <p>
                    To revolutionize healthcare follow-ups through intelligent automation,
                    ensuring every patient receives seamless post-hospital care.
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class='vision-card'>
                <img src='https://cdn-icons-png.flaticon.com/512/3209/3209265.png' width='80'>
                <h4>Our Mission</h4>
                <p>
                    To empower hospitals and caregivers with AI-driven tools that enhance
                    communication, monitor recovery, and improve patient satisfaction.
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class='vision-card'>
                <img src='https://cdn-icons-png.flaticon.com/512/2867/2867295.png' width='80'>
                <h4>What We Do</h4>
                <p>
                    CareLoop.AI bridges the gap between hospitals and patients,
                    enabling smart follow-up calls, feedback collection, and analytics-driven insights.
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        "<p style='text-align:center;color:#14b8a6;font-size:14px;'>© 2025 CareLoop.AI | Empowering Connected Healthcare</p>",
        unsafe_allow_html=True
    )

elif menu == "Patient List":
    st.subheader("📋 Patient List")

    response = requests.get(f"{API_URL}/patient")
    if response.status_code in (200, 201):
        patients = response.json()

        if not patients:
            st.info("No patients found.")
        else:
            if "edit_patient_id" not in st.session_state:
                st.session_state.edit_patient_id = None

            # Create header row
            st.markdown("---")
            header_cols = st.columns([2, 0.8, 1.2, 2, 2, 1.8, 3, 1.8, 1.2])
            header_cols[0].markdown("**Name**")
            header_cols[1].markdown("**Age**")
            header_cols[2].markdown("**Gender**")
            header_cols[3].markdown("**Phone**")
            header_cols[4].markdown("**Disease**")
            header_cols[5].markdown("**Visit Date**")
            header_cols[6].markdown("**Medication**")
            header_cols[7].markdown("**Next Visit**")
            header_cols[8].markdown("**Actions**")
            st.markdown("---")

            for patient in patients:
                cols = st.columns([2, 0.8, 1.2, 2, 2, 1.8, 3, 1.8, 1.2])

                cols[0].write(patient["name"])
                cols[1].write(patient["age"])
                cols[2].write(patient["gender"])
                cols[3].write(patient["phone"])
                cols[4].write(patient["disease"])
                cols[5].write(patient["visit_date"])
                cols[6].write(", ".join(patient["prescribed_medication"]))
                cols[7].write(patient["next_visit_date"])

                with cols[8]:
                    col_edit, col_delete = st.columns(2)
                    with col_edit:
                        edit_btn = st.button("✏️", key=f"edit_{patient['_id']}", help="Edit Patient")
                    with col_delete:
                        delete_btn = st.button("🗑️", key=f"delete_{patient['_id']}", help="Delete Patient")

                if edit_btn:
                    st.session_state.edit_patient_id = patient["_id"]
                    st.rerun()

                if delete_btn:
                    delete_response = requests.delete(f"{API_URL}/patient/{patient['_id']}")
                    if delete_response.status_code in (200, 204):
                        st.warning(f"🗑️ Deleted {patient['name']} successfully!")
                        st.session_state.edit_patient_id = None
                        st.rerun()
                    else:
                        st.error("❌ Failed to delete patient.")

            if st.session_state.edit_patient_id:
                st.markdown("---")
                patient_to_edit = next(
                    (p for p in patients if p["_id"] == st.session_state.edit_patient_id),
                    None
                )
                if patient_to_edit:
                    with st.form(f"edit_form_{patient_to_edit['_id']}"):
                        st.subheader(f"✏️ Edit Details for {patient_to_edit['name']}")
                        name = st.text_input("Name", value=patient_to_edit["name"])
                        age = st.number_input("Age", min_value=0, max_value=120, value=patient_to_edit["age"])
                        gender = st.selectbox(
                            "Gender", ["Male", "Female"],
                            index=0 if patient_to_edit["gender"] == "Male" else 1
                        )
                        phone = st.text_input("Phone", value=patient_to_edit["phone"])
                        disease = st.text_input("Disease", value=patient_to_edit["disease"])
                        # visit_date = st.text_input("Visit Date", value=patient_to_edit["visit_date"])
                        try:
                            visit_date_default = datetime.strptime(patient_to_edit["visit_date"], "%Y-%m-%d").date()
                        except:
                            visit_date_default = date.today()
                        visit_date = st.date_input("Visit Date", value=visit_date_default)
                        prescribed_medication = st.text_area(
                            "Prescribed Medication",
                            value=", ".join(patient_to_edit["prescribed_medication"])
                        )
                        # next_visit_date = st.text_input("Next Visit Date", value=patient_to_edit["next_visit_date"])
                        try:
                            next_visit_default = datetime.strptime(patient_to_edit["next_visit_date"],
                                                                   "%Y-%m-%d").date()
                        except:
                            next_visit_default = None
                        next_visit_date = st.date_input("Next Visit Date", value=next_visit_default)

                        col_update, col_cancel = st.columns(2)
                        with col_update:
                            submit_edit = st.form_submit_button("Update Patient")
                        with col_cancel:
                            cancel_edit = st.form_submit_button("Cancel")

                        if submit_edit:
                            updated_data = {
                                "name": name,
                                "age": age,
                                "gender": gender,
                                "phone": phone,
                                "disease": disease,
                                "visit_date": str(visit_date),
                                "prescribed_medication": [pm.strip() for pm in prescribed_medication.split(",")],
                                "next_visit_date": str(next_visit_date)
                            }
                            update_response = requests.put(
                                f"{API_URL}/patient/{patient_to_edit['_id']}", json=updated_data
                            )
                            if update_response.status_code in (200, 201):
                                st.success(f"✅ {name} updated successfully!")
                                st.session_state.edit_patient_id = None
                                st.rerun()
                            else:
                                st.error("Failed to update patient details.")

                        if cancel_edit:
                            st.session_state.edit_patient_id = None
                            st.rerun()
    else:
        st.error("Error fetching patient data.")

elif menu == "Start Patient Follow-Up":
    st.subheader("📞 Start Patient Follow-Up")
    res = requests.get(f"{API_URL}/patient/pending-followup-patients")
    patients = res.json()
    name_pres = [pat["name"] for pat in patients if "name" in pat]

    if name_pres:
        options = ["-- Select a patient --"] + name_pres
        sel_name = st.selectbox("Select Patient Name", options, key="patient_select")

        # Only show details if a valid patient is selected
        if sel_name != "-- Select a patient --":
            patient_sel = [p for p in patients if p["name"] == sel_name]
            if patient_sel:
                pati = patient_sel[0]

                st.markdown("---")
                st.write("### 📋 Selected Patient Details:")

                # Create a nice card layout for patient details
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Name:** {pati['name']}")
                    st.write(f"**Age:** {pati['age']}")
                    st.write(f"**Gender:** {pati['gender']}")
                with col2:
                    st.write(f"**Phone:** {pati['phone']}")
                    st.write(f"**Visit Date:** {pati['visit_date']}")

                st.write(f"**Prescribed Medication:** {', '.join(pati['prescribed_medication'])}")

                if "followup_started" not in st.session_state:
                    st.session_state.followup_started = False

                st.markdown("---")
                if not st.session_state.followup_started:
                    if st.button("📞 Start Patient Follow-Up"):
                        try:
                            call_data = {
                                "patient_id": pati["_id"],  # <-- ADD THIS LINE
                                "name": pati["name"],
                                "phone": pati["phone"]
                            }
                            call_res = requests.post(f"{CALL_API_URL}/patient/call_number", json=call_data)

                            if call_res.status_code == 200:
                                st.success(f"Initiating AI call to {pati['name']} ...")
                                time.sleep(2)
                                # st.info("Call connected. AI is greeting the patient by name.")
                            else:
                                st.error("Failed to initiate call. Please check backend logs.")
                        except Exception as e:
                            st.error(f"Error connecting to backend: {e}")

        else:
            st.info("👆 Please select a patient from the dropdown to view details and start follow-up.")
    else:
        st.error("No Patients Found")

if "selected_call_record" not in st.session_state:
    st.session_state.selected_call_record = None

elif menu == "Patient Feedback":
    st.subheader("💬 Patient Feedback Summary")

    # --- VIEW 1: Show the chat for the selected call ---
    if st.session_state.selected_call_record:
        record = st.session_state.selected_call_record
        patient_name = record.get('patient_name', 'Unknown Patient')
        call_date = record.get('start_time', '').split('T')[0]

        st.markdown(f"### Chat History for {patient_name}")
        st.markdown(f"**Call Date:** {call_date}")

        # --- (3) DISPLAY SUMMARY METRICS ---
        st.markdown("#### Call Summary:")
        col1_sum, col2_sum, col3_sum = st.columns(3)

        # Overall Sentiment
        sentiment = record.get('overall_sentiment', 'UNCLEAR')
        sentiment_emoji = get_sentiment_emoji(sentiment)
        with col1_sum:
            st.metric(label="Overall Sentiment", value=f"{sentiment_emoji} {sentiment}")

        # Medication Adherence
        adherence = record.get('medical_adherence', 'UNCLEAR')
        adherence_emoji = get_adherence_emoji(adherence)
        with col2_sum:
            st.metric(label="Medication Adherence", value=f"{adherence_emoji} {adherence}")

        # Side Effects Reported
        side_effects = record.get('side_effects_reported', False)
        side_effects_display = get_side_effects_display(side_effects)
        with col3_sum:
            st.metric(label="Side Effects", value=side_effects_display)

        st.markdown("---")

        # Dynamically build the chat HTML
        chat_html = ""
        for entry in record['transcript']:
            if entry['speaker'] == 'Assistant':
                chat_html += f"<div class='message ai'><b>🤖 AI:</b> {entry['text']}</div>"
            else:
                chat_html += f"<div class='message user'><b>🧑 Patient:</b> {entry['text']}</div>"

        st.markdown(f"""
        <div class="chat-box">
            {chat_html}
        </div>
        """, unsafe_allow_html=True)

        if st.button("⬅ Back to Call List"):
            st.session_state.selected_call_record = None
            st.rerun()

    # --- VIEW 2: Show the list of all calls ---
    else:
        tb1, tb2, tb3 = st.tabs(["Call History", "Summary", "Medication Details"])

        with tb1:
            st.subheader("Recent Call History")
            try:
                res = requests.get(f"{API_URL}/patient/call-records")
                if res.status_code == 200:
                    call_records = res.json()
                    if not call_records:
                        st.info("No call records found.")
                    else:
                        cols = st.columns([2, 2, 2, 1])
                        cols[0].markdown("**Patient Name**")
                        cols[1].markdown("**Call Duration**")
                        cols[2].markdown("**Sentiment**")  # Renamed column
                        cols[3].markdown("**Action**")
                        st.markdown("---")

                        for record in call_records:
                            cols = st.columns([2, 2, 2, 1])
                            cols[0].write(record.get('patient_name', 'N/A'))
                            duration = calculate_duration(record.get('start_time', ''), record.get('end_time', ''))
                            cols[1].write(duration)
                            sentiment = record.get('overall_sentiment', 'N/A')
                            emoji = get_sentiment_emoji(sentiment)
                            cols[2].write(f"{emoji} {sentiment}")
                            # Use record['_id'] which comes from the API now
                            record_id = record.get('_id', record.get('id'))  # Handle both possibilities
                            if record_id and cols[3].button("💬", key=f"chat_{record_id}", help="View Chat"):
                                st.session_state.selected_call_record = record
                                st.rerun()
                else:
                    st.error(f"Failed to fetch call records: {res.text}")
            except Exception as e:
                st.error(f"Error processing data: {e}")

        with tb2:
            st.info("Here comes the patient summary or call summary")

        with tb3:
            st.info("Here comes the patient medication details")

elif menu == "Appointments":
    st.title("📅 Confirmed Appointments")

    # Define the column layout
    # [Patient Name, Department, Date, Time, Status]
    column_weights = [3, 2.5, 2, 1.5, 2]
    column_headers = ["Patient Name", "Department", "Date", "Time", "Status"]

    confirmed_tab, past_tab = st.tabs([
        "Upcoming Appointments", "Past Appointments"
    ])

    with confirmed_tab:
        st.subheader("Upcoming Confirmed Appointments")
        try:
            res = requests.get(f"{API_URL}/appointments", params={"view": "active"})
            if res.status_code == 200:
                active_appointments = res.json()
                if not active_appointments:
                    st.info("No upcoming confirmed appointments found.")
                else:
                    # --- Create Header Row ---
                    st.divider()
                    header_cols = st.columns(column_weights)
                    for i, header in enumerate(column_headers):
                        header_cols[i].markdown(f"**{header}**")
                    st.divider()

                    # --- Create Data Rows ---
                    for appt in active_appointments:
                        cols = st.columns(column_weights)
                        cols[0].write(appt.get('patient_name', 'N/A'))
                        cols[1].write(appt.get('department', 'N/A'))
                        cols[2].write(appt.get('appointment_date', 'N/A'))
                        cols[3].write(appt.get('appointment_time', 'N/A'))
                        status = appt.get('status', 'N/A')
                        if status == "Confirmed":
                            cols[4].markdown(f"✅ **{status}**")
                        else:
                            cols[4].write(status)

            else:
                st.error(f"Failed to fetch active appointments: {res.text}")
        except Exception as e:
            st.error(f"Error connecting to appointments API: {e}")

    with past_tab:
        st.subheader("Past Appointments History")
        try:
            res = requests.get(f"{API_URL}/appointments", params={"view": "past"})
            if res.status_code == 200:
                past_appointments = res.json()
                if not past_appointments:
                    st.info("No past appointment history found.")
                else:
                    # --- Create Header Row ---
                    st.divider()
                    header_cols = st.columns(column_weights)
                    for i, header in enumerate(column_headers):
                        header_cols[i].markdown(f"**{header}**")
                    st.divider()

                    # --- Create Data Rows ---
                    for appt in past_appointments:
                        cols = st.columns(column_weights)
                        cols[0].write(appt.get('patient_name', 'N/A'))
                        cols[1].write(appt.get('department', 'N/A'))
                        cols[2].write(appt.get('appointment_date', 'N/A'))
                        cols[3].write(appt.get('appointment_time', 'N/A'))
                        status = appt.get('status', 'N/A')
                        # Status here will be 'Visited' based on DB logic
                        if status == "Visited":
                            cols[4].markdown(f"✔️ {status}")
                        else:
                            cols[4].write(status)
            else:
                st.error(f"Failed to fetch past appointments: {res.text}")
        except Exception as e:
            st.error(f"Error fetching past appointments: {e}")


elif menu == "Analytics":

    total_patients = "N/A"
    total_engaged = "N/A"
    total_alerts = "N/A"
    alert_delta_text = None
    alert_delta_color = "normal"

    # --- Fetch Metrics ---
    try:
        # Get total patients count
        patients_res = requests.get(f"{API_URL}/patient")
        if patients_res.status_code == 200:
            total_patients = len(patients_res.json())
        else:
            st.warning("Could not fetch total patient count.")

        # Get engagement and alert metrics
        metrics_res = requests.get(f"{API_URL}/patient/metrics")
        if metrics_res.status_code == 200:
            metrics_data = metrics_res.json()
            total_engaged = metrics_data.get('total_patients_engaged', 0)
            total_alerts = metrics_data.get('total_flagged_alerts', 0)
            if total_alerts > 0:
                alert_delta_text = f"{total_alerts} High Priority"
                alert_delta_color = "inverse"  # Makes delta red
        else:
            st.warning("Could not fetch dashboard metrics.")

    except Exception as e:
        st.error(f"Error connecting to API: {e}")
    # --- End Fetch Metrics ---

    st.subheader("📊 Key Metrics")  # Changed subheader
    # st.write("Visual insights and performance overview") # Optional text

    # --- Display Dynamic Metric Cards ---
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
                    <div class="metric-card">
                        <img src="https://cdn-icons-png.flaticon.com/512/4320/4320371.png" width="60">
                        <div class="metric-label">Total Patients</div>
                        <div class="metric-value">{total_patients}</div>
                    </div>
                    """, unsafe_allow_html=True)
    with col2:
        # Using a phone/call icon for engaged
        st.markdown(
            f"""
                    <div class="metric-card">
                        <img src="https://cdn-icons-png.flaticon.com/512/455/455705.png" width="60">
                        <div class="metric-label">Patients Engaged</div>
                        <div class="metric-value">{total_engaged}</div>
                    </div>
                    """, unsafe_allow_html=True)

    with col3:
        # Using the existing alert icon
        st.markdown(
            f"""
                    <div class="metric-card">
                        <img src="https://cdn-icons-png.flaticon.com/512/7249/7249210.png" width="60">
                        <div class="metric-label">Active Alerts</div>
                        <div class="metric-value">{total_alerts}</div>
                    </div>
                    """, unsafe_allow_html=True)
        # Optionally add the delta text below the card if needed,
        # st.metric doesn't integrate well with custom HTML cards
        # if alert_delta_text:
        #     st.markdown(f"<p style='text-align:center; color: #ef4444;'>{alert_delta_text}</p>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<h3 style="color: #14b8a6; margin-top: 40px;">📈 Insights Overview</h3>', unsafe_allow_html=True)
    col_left, col_right = st.columns(2)

    call_records = []
    try:
        records_res = requests.get(f"{API_URL}/patient/call-records")
        if records_res.status_code == 200:
            call_records = records_res.json()
        else:
            st.warning("Could not fetch call records for charts.")
    except Exception as e:
        st.error(f"Error connecting to API for call records: {e}")

    # --- Generate Charts ---
    col_left, col_right = st.columns(2)

    # 1. Sentiment Pie Chart
    with col_left:
        st.subheader("Follow-up Sentiment")
        fig1, ax1 = plt.subplots(facecolor='#0a1e2b')  # Keep background styling
        ax1.set_facecolor('#0a1e2b')

        if call_records:
            sentiments = [record.get('overall_sentiment', 'NEUTRAL') for record in call_records]
            sentiment_counts = Counter(sentiments)

            # Ensure order and presence of all categories
            labels = ["POSITIVE", "NEUTRAL", "ALERT"]
            sizes = [sentiment_counts.get(label, 0) for label in labels]
            colors = ['#06b6d4', '#a7f3d0', '#044954']

            # Filter out zero-value slices to avoid display issues
            non_zero_labels = [label for i, label in enumerate(labels) if sizes[i] > 0]
            non_zero_sizes = [size for size in sizes if size > 0]
            non_zero_colors = [color for i, color in enumerate(colors) if sizes[i] > 0]

            if non_zero_sizes:  # Only plot if there's data
                ax1.pie(non_zero_sizes, labels=non_zero_labels, autopct='%1.1f%%', startangle=90,
                        colors=non_zero_colors,
                        textprops={'color': '#e8f5f7', 'fontsize': 12, 'weight': 'bold'})
                ax1.axis('equal')
            else:
                ax1.text(0.5, 0.5, 'No Sentiment Data', horizontalalignment='center', verticalalignment='center',
                         color='#e8f5f7')
                ax1.axis('off')  # Hide axes if no data
        else:
            ax1.text(0.5, 0.5, 'No Call Records Found', horizontalalignment='center', verticalalignment='center',
                     color='#e8f5f7')
            ax1.axis('off')  # Hide axes if no data

        st.pyplot(fig1)

    # 2. Adherence Bar Chart
    with col_right:
        st.subheader("Medication Adherence")
        fig2, ax2 = plt.subplots(facecolor='#0a1e2b')
        ax2.set_facecolor('#0a1e2b')

        if call_records:
            # Get the CLASSIFIED adherence status directly
            adherence_statuses_raw = [
                record.get('medical_adherence', 'NOT_ASKED')  # Default to UNCLEAR if missing
                for record in call_records
            ]
            adherence_statuses = [
                "UNCLEAR" if status == "NOT_ASKED" else status
                for status in adherence_statuses_raw
            ]
            adherence_counts = Counter(adherence_statuses)

            # Define categories based on the classification output
            categories = ["ADHERENT", "NON-ADHERENT", "UNCLEAR"]
            values = [adherence_counts.get(cat, 0) for cat in categories]
            bar_colors = ["#14b8a6", "#044954", "#a7f3d0"]

            if any(v > 0 for v in values):  # Only plot if there's data
                bars = ax2.bar(categories, values, color=bar_colors)
                ax2.set_ylabel("Number of Patients", color='#e8f5f7', fontweight='bold')
                ax2.tick_params(axis='x', colors='#e8f5f7')
                ax2.tick_params(axis='y', colors='#e8f5f7')
                ax2.spines['bottom'].set_color('#14b8a6')
                ax2.spines['left'].set_color('#14b8a6')
                ax2.spines['top'].set_visible(False)
                ax2.spines['right'].set_visible(False)
                ax2.bar_label(bars, color='#e8f5f7', padding=3)  # Add counts on top
            else:
                ax2.text(0.5, 0.5, 'No Adherence Data', transform=ax2.transAxes,  # Use axes coordinates
                         horizontalalignment='center',
                         verticalalignment='center',
                         color='#e8f5f7')
                ax2.axis('off')
        else:
            ax2.text(0.5, 0.5, 'No Call Records Found', transform=ax2.transAxes,  # Use axes coordinates
                     horizontalalignment='center',
                     verticalalignment='center',
                     color='#e8f5f7')
            ax2.axis('off')

        st.pyplot(fig2)

elif menu == "Logout":
    st.session_state.clear()
    st.success("You have been logged out successfully.")
    time.sleep(1)
    st.switch_page("ui_file.py")

