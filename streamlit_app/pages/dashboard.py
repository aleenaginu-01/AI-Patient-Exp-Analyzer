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
import math
import json

load_dotenv(override=True)
API_URL = os.getenv("API_URL")
CALL_API_URL = os.getenv("CALL_API_URL")


# --- HELPER FUNCTIONS (Unchanged) ---
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
        return "🚩"  # Red flag for alerts
    if sentiment == "NEGATIVE":
        return "❌"  # Should be rare, as it's covered by ALERT
    return "➖"


def get_adherence_emoji(adherence: str) -> str:
    """Returns an emoji for the adherence classification."""
    if adherence == "ADHERENT":
        return "✅"  # Checkmark
    if adherence == "NON-ADHERENT":
        return "⚠️"  # Warning sign
    return "❓"  # Question mark for Unclear


def get_side_effects_display(reported: bool) -> str:
    """Returns an emoji and text for side effects status."""
    if reported:
        return "❗ Reported"  # Exclamation for reported
    return "➖ None Reported"

# --- END HELPER ---
if "patient_list_page" not in st.session_state:
    st.session_state.patient_list_page = 0
if "edit_patient_id" not in st.session_state:
    st.session_state.edit_patient_id = None

st.set_page_config(page_title="Admin Dashboard", layout="wide")

# --- REFACTORED CSS: Light Hospital Theme ---
hide_default_format = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        * {
            font-family: 'Inter', sans-serif;
        }

        /* Hide Streamlit branding */
        header[data-testid="stHeader"] {display: none;}
        [data-testid="stSidebarNav"] {display: none;}
        [data-testid="stSidebarNavItems"] {display: none;}
        [data-testid="stToolbar"] {display: none;}
        footer {display: none;}

        /* Main App Background */
        .stApp {
            background-color: #c2ffec;
            color: #333333;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color:#b9f0de;
            border-right: 1px solid #E0E0E0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: #1A2B4D;
        }

        /* Sidebar Header */
        [data-testid="stSidebar"] h1 {
            color: #245444 !important;
            font-size: 28px !important;
            font-weight: 700 !important;
            text-align: center;
            padding: 20px 0;
            margin-bottom: 10px;
        }

        /* Sidebar Radio Buttons */
        [data-testid="stSidebar"] .stRadio > label {
            color: #245444 !important;
            font-weight: 600 !important;
            font-size: 16px !important;
            margin-bottom: 15px !important;
        }

        [data-testid="stSidebar"] .stRadio > div {
            gap: 8px;
        }

        /* Styling the individual radio option labels */
        [data-testid="stSidebar"] .stRadio label {
            background: #d4faf1;
            padding: 14px 20px;
            border-radius: 10px;
            transition: all 0.3s ease;
            border: 1px solid transparent;
            color: #333333 !important;
            font-size: 15px !important;
            display: block;
            width: 100%;
        }

        [data-testid="stSidebar"] .stRadio label:hover {
            background: #9ae6d4;
            border-color: #112e27;
            transform: translateX(5px);
            color: #0056B3 !important;
        }

        /* This selector targets the label of the *checked* radio button */
        [data-testid="stSidebar"] .stRadio div[data-checked="true"] label {
            background-color: #007BFF !important;
            color: #FFFFFF !important;
            border-color: #0056B3 !important;
            font-weight: 500;
        }


        /* Main Header */
        h1, h2, h3 {
            color: #245444 !important;
            font-weight: 600 !important;
        }

        h1 {
            font-size: 42px !important;
            text-align: center;
            margin-bottom: 10px !important;
            animation: fadeInDown 0.8s ease;
        }

        h2 {
            font-size: 28px !important;
            margin-top: 30px !important;
            color: #245444 !important;
        }

        h3 {
            font-size: 22px !important;
        }

        /* Subheader styling */
        .stMarkdownContainer h3 {
            color: #007BFF !important;
            font-weight: 600;
        }

        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #007BFF 0%, #0056B3 100%);
            color: white !important;
            border: none;
            border-radius: 10px;
            padding: 12px 28px;
            font-weight: 600;
            font-size: 15px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 123, 255, 0.2);
        }

        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 25px rgba(0, 123, 255, 0.3);
            background: linear-gradient(135deg, #0056B3 0%, #004085 100%);
        }

        /* --- LIGHT THEME INPUT FIELDS --- */

        /* Text/Number/Textarea Inputs */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stTextArea textarea {
            background-color: #FFFFFF !important;
            border: 1.5px solid #CED4DA !important;
            border-radius: 10px !important;
            color: #333333 !important;
            padding: 10px !important;
        }

        /* Selectbox Container */
        .stSelectbox {
            color: #FFFFFF !important;
        }

        /* Selectbox Input Wrapper */
        .stSelectbox > div > div {
            background: #FFFFFF !important;
            border: 1.5px solid #CED4DA !important;
            border-radius: 10px !important;
        }

        /* Selectbox - the actual select element */
        .stSelectbox select {
            background: #FFFFFF !important;
            color: #333333 !important;
            border: none !important;
        }

        /* Selectbox - BaseWeb Select component */
        .stSelectbox div[data-baseweb="select"] {
            background: #FFFFFF !important;
        }

        /* Selectbox - Selected value container */
        .stSelectbox div[data-baseweb="select"] > div {
            background: #FFFFFF !important;
            border: none !important; /* Managed by wrapper */
            border-radius: 10px !important;
        }

        /* Selectbox - Selected value text */
        .stSelectbox div[data-baseweb="select"] > div > div {
            color: #333333 !important;
        }

        /* Selectbox - All text inside */
        .stSelectbox * {
            color: #333333 !important;
        }

        /* Selectbox dropdown menu */
        div[data-baseweb="popover"] {
            background: #FFFFFF !important;
            border: 1px solid #CED4DA !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        /* Selectbox dropdown list */
        ul[role="listbox"] {
            background: #FFFFFF !important;
        }

        /* Selectbox dropdown options */
        li[role="option"] {
            background: #FFFFFF !important;
            color: #333333 !important;
        }

        /* Selectbox dropdown options hover */
        li[role="option"]:hover {
            background: #F1F3F5 !important;
            color: #1A2B4D !important;
        }

        /* Selectbox dropdown selected option */
        li[role="option"][aria-selected="true"] {
            background: #E0E7FF !important;
            color: #0056B3 !important;
        }

        /* Date Input Styling */
        .stDateInput > div > div {
            background: #FFFFFF !important;
            border: 1.5px solid #CED4DA !important;
            border-radius: 10px !important;
        }

        .stDateInput input {
            background: #FFFFFF !important;
            color: #333333 !important;
            border: none !important;
        }

        /* Date picker calendar styling */
        .stDateInput div[data-baseweb="calendar"] {
            background: #FFFFFF !important;
            border: 1px solid #CED4DA !important;
        }

        /* Calendar dates */
        .stDateInput button {
            color: #333333 !important;
        }

        /* Calendar selected date */
        .stDateInput button[aria-selected="true"] {
            background: #007BFF !important;
            color: white !important;
        }

        /* Calendar hover */
        .stDateInput button:hover {
            background: #E0E7FF !important ;
        }

        /* Input Focus State */
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus,
        .stSelectbox > div > div:focus-within,
        .stTextArea textarea:focus,
        .stDateInput > div > div:focus-within {
            border-color: #007BFF !important;
            box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.15) !important;
        }

        /* Labels */
        .stTextInput > label,
        .stNumberInput > label,
        .stSelectbox > label,
        .stDateInput > label,
        .stTextArea > label {
            color: #1A2B4D !important;
            font-weight: 500 !important;
            font-size: 15px !important;
        }

        /* --- END LIGHT THEME INPUTS --- */


        /* Cards & Containers */
        .stContainer {
            background: #FFFFFF;
            border: 1px solid #E0E0E0;
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
            transition: all 0.3s ease;
            animation: fadeIn 0.5s ease;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }

        .stContainer:hover {
            border-color: #007BFF;
            box-shadow: 0 5px 20px rgba(0, 123, 255, 0.1);
        }

        /* DataFrames */
        .stDataFrame {
            border: 1px solid #DEE2E6;
            border-radius: 10px;
            overflow: hidden;
        }

        /* Success/Error/Warning Messages */
        .stSuccess {
            background-color: #D4EDDA !important;
            color: #155724 !important;
            border: 1px solid #C3E6CB !important;
        }

        .stError {
            background-color: #F8D7DA !important;
            color: #721C24 !important;
            border: 1px solid #F5C6CB !important;
        }

        .stWarning {
            background-color: #FFF3CD !important;
            color: #856404 !important;
            border: 1px solid #FFEAA7 !important;
        }

        .stInfo {
            background-color: #D1ECF1 !important;
            color: #0C5460 !important;
            border: 1px solid #BEE5EB !important;
        }

        /* Divider */
        hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, #CED4DA, transparent);
            margin: 30px 0;
        }

        /* File Uploader */
        [data-testid="stFileUploader"] {
            background: #F8F9FA;
            border: 2px dashed #007BFF;
            border-radius: 10px;
            padding: 20px;
        }
        [data-testid="stFileUploader"] * {
            color: #333333;
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }

        .stTabs [data-baseweb="tab"] {
            background: #E9ECEF;
            border-radius: 8px;
            color: #5A6A7B;
            padding: 10px 20px;
        }

        .stTabs [aria-selected="true"] {
            background: #007BFF;
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

        /* Custom metric cards */
        .metric-card {
            background: #FFFFFF;
            border: 1px solid #E0E0E0;
            color: #245444;
            text-align: center;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
            margin: 10px;
            animation: fadeIn 0.6s ease;
        }

        .metric-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 8px 25px rgba(0, 123, 255, 0.15);
            border-color: #245444;
        }

        .metric-label {
            font-size: 16px;
            font-weight: 500;
            margin-top: 15px;
            color: #245444;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .metric-value {
            font-size: 36px;
            font-weight: 700;
            color: #245444;
        }

        /* Chat box styling */
        .chat-box {
            background: #F8F9FA;
            border: 1px solid #DEE2E6;
            border-radius: 15px;
            padding: 20px;
            height: 400px;
            overflow-y: auto;
            font-family: 'Inter', sans-serif;
            font-size: 15px;
            color: #333333;
            box-shadow: inset 0 2px 8px rgba(0,0,0,0.05);
        }

        .message {
            margin: 12px 0;
            padding: 12px 18px;
            border-radius: 12px;
            width: fit-content;
            max-width: 75%;
            animation: fadeIn 0.4s ease;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }

        .ai {
            background: #FFFFFF;
            border: 1px solid #E0E0E0;
            color: #333333;
            text-align: left;
            border-left: 3px solid #007BFF;
        }

        .user {
            background: #E0E7FF;
            color: #1A2B4D;
            text-align: left; /* Keep left align for readability */
            margin-left: auto;
            border-right: 3px solid #0056B3;
        }

        /* Vision/Mission cards */
        .vision-card {
            background: #FFFFFF;
            padding: 30px;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            border: 1px solid #E0E0E0;
            transition: all 0.4s ease;
            animation: fadeIn 0.8s ease;
            height: 100%; /* Make cards same height */
        }

        .vision-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 12px 35px rgba(0, 123, 255, 0.15);
            border-color: #245444;
        }

        .vision-card h4 {
            color: #245444 !important;
            font-size: 22px !important;
            font-weight: 600 !important;
            margin: 15px 0 !important;
        }

        .vision-card p {
            color: #5A6A7B !important;
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
        [data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #E0E0E0;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    transition: all 0.3s ease;
}

    [data-testid="stMetric"]:hover {
        border-color: #007BFF;
        box-shadow: 0 5px 20px rgba(0, 123, 255, 0.1);
    }
    
    /* This styles the LABEL (e.g., "Overall Sentiment") */
    [data-testid="stMetricLabel"] {
        color: #5A6A7B !important; /* Dark grey, legible label */
        font-size: 16px;
        font-weight: 500;
    }
    
    /* This styles the VALUE (e.g., "✅ POSITIVE") */
    [data-testid="stMetricValue"] {
        color: #1A2B4D !important; /* Darkest, primary value color */
        font-size: 28px;
        font-weight: 600;
    }
    /* --- Call Status Container --- */
    .call-status-container {
        background: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 15px;
        padding: 40px;
        max-width: 450px;
        margin: 30px auto;
        box-shadow: 0 8px 30px rgba(0,0,0,0.08);
        text-align: center;
    }
    .call-status-icons {
        font-size: 48px;
        margin-bottom: 25px;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 30px;
    }
    .call-status-text {
        font-size: 20px;
        font-weight: 600;
        color: #1A2B4D;
    }
    .call-status-subtext {
        font-size: 15px;
        color: #5A6A7B;
        margin-top: 10px;
    }
    /* --- Add Patient Submit Button Style --- */
    .add-patient-form-button .stButton > button {
        width: 100%; 
        background: linear-gradient(135deg, #8debd2 0%, #62b59f 100%) !important;
        color: black !important;
        border: none;
        padding: 16px 30px;
        font-size: 16px;
        font-weight: 600;
        border-radius: 12px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(98, 181, 159, 0.3); /* I updated the shadow color for you */
    }
        </style> 
"""
st.markdown(hide_default_format, unsafe_allow_html=True)

st.header("🏥 CareLoop.AI")
st.sidebar.header("CareLoop.AI")
st.sidebar.title("Admin Panel")

menu = st.sidebar.radio(
    "Select View:",
    ["Dashboard", "Add Patients", "Patient List", "Start Patient Follow-Up", "Patient Feedback", "Analytics",
     "Appointments", "Logout"],
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
        visit_date = st.date_input("Visit Date", value=date.today())
        pre_medi = st.text_input("Prescribed Medication (comma-separated)")
        next_visit_date = st.date_input("Next Visit Date", value=date.today())
        st.markdown('<div class="add-patient-form-button">', unsafe_allow_html=True)
        submitted = st.form_submit_button("Add Patient")
        st.markdown('</div>', unsafe_allow_html=True)
        # submitted = st.form_submit_button("Add Patient")
        if submitted:
            if not name.strip() or not phone.strip() or not disease.strip() or not pre_medi.strip() or age == 0:
                st.error("⚠️ All fields are required. Please fill in all details and set a valid age.")
            else:
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
                try:
                    response = requests.post(API_URL + "/patient", json=patient_data)
                    if response.status_code in (200, 201):
                        st.success(f"Patient {name} added successfully!")
                    else:
                        st.error(f"Error adding patient {response.text}")
                except Exception as e:
                    st.error(f"Error connecting to API: {e}")

elif menu == "Dashboard":
    st.title("Admin Dashboard")
    total_patients = "N/A"
    total_engaged = "N/A"
    total_alerts = "N/A"
    alert_delta_text = None
    alert_delta_color = "normal"

    # --- Fetch Metrics ---
    try:
        patients_res = requests.get(f"{API_URL}/patient")
        if patients_res.status_code == 200:
            total_patients = len(patients_res.json())
        else:
            st.warning("Could not fetch total patient count.")

        metrics_res = requests.get(f"{API_URL}/patient/metrics")
        if metrics_res.status_code == 200:
            metrics_data = metrics_res.json()
            total_engaged = metrics_data.get('total_patients_engaged', 0)
            total_alerts = metrics_data.get('total_flagged_alerts', 0)
            if total_alerts > 0:
                alert_delta_text = f"{total_alerts} High Priority"
                alert_delta_color = "inverse"
        else:
            st.warning("Could not fetch dashboard metrics.")

    except Exception as e:
        st.error(f"Error connecting to API: {e}")
    # --- End Fetch Metrics ---

    st.subheader("📊 Key Metrics")

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
        st.markdown(
            f"""
                <div class="metric-card">
                    <img src="https://cdn-icons-png.flaticon.com/512/455/455705.png" width="60">
                    <div class="metric-label">Patients Engaged</div>
                    <div class="metric-value">{total_engaged}</div>
                </div>
                """, unsafe_allow_html=True)

    with col3:
        st.markdown(
            f"""
                <div class="metric-card">
                    <img src="https://cdn-icons-png.flaticon.com/512/7249/7249210.png" width="60">
                    <div class="metric-label">Active Alerts</div>
                    <div class="metric-value">{total_alerts}</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<h3 style="color: #007BFF; margin-top: 40px;">📈 Insights Overview</h3>', unsafe_allow_html=True)

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
        # STYLING CHANGE: Updated facecolor to white
        fig1, ax1 = plt.subplots(facecolor='#FFFFFF')
        ax1.set_facecolor('#FFFFFF')

        if call_records:
            sentiments = [record.get('overall_sentiment', 'NEUTRAL') for record in call_records]
            sentiment_counts = Counter(sentiments)

            labels = ["POSITIVE", "NEUTRAL", "ALERT"]
            sizes = [sentiment_counts.get(label, 0) for label in labels]
            # STYLING CHANGE: Updated colors to blue/grey/red palette
            colors = ['#69dbf0', '#25acc4', '#14515c']

            non_zero_labels = [label for i, label in enumerate(labels) if sizes[i] > 0]
            non_zero_sizes = [size for size in sizes if size > 0]
            non_zero_colors = [color for i, color in enumerate(colors) if sizes[i] > 0]

            if non_zero_sizes:
                ax1.pie(non_zero_sizes, labels=non_zero_labels, autopct='%1.1f%%', startangle=90,
                        colors=non_zero_colors,
                        # STYLING CHANGE: Updated text color to dark
                        textprops={'color': '#333333', 'fontsize': 12, 'weight': 'bold'})
                ax1.axis('equal')
            else:
                # STYLING CHANGE: Updated text color to dark
                ax1.text(0.5, 0.5, 'No Sentiment Data', horizontalalignment='center', verticalalignment='center',
                         color='#333333')
                ax1.axis('off')
        else:
            # STYLING CHANGE: Updated text color to dark
            ax1.text(0.5, 0.5, 'No Call Records Found', horizontalalignment='center', verticalalignment='center',
                     color='#333333')
            ax1.axis('off')

        st.pyplot(fig1)

    # 2. Adherence Bar Chart
    with col_right:
        st.subheader("Medication Adherence")
        # STYLING CHANGE: Updated facecolor to white
        fig2, ax2 = plt.subplots(facecolor='#FFFFFF')
        ax2.set_facecolor('#FFFFFF')

        if call_records:
            adherence_statuses_raw = [
                record.get('medical_adherence', 'NOT_ASKED')
                for record in call_records
            ]
            adherence_statuses = [
                "UNCLEAR" if status == "NOT_ASKED" else status
                for status in adherence_statuses_raw
            ]
            adherence_counts = Counter(adherence_statuses)

            categories = ["ADHERENT", "NON-ADHERENT", "UNCLEAR"]
            values = [adherence_counts.get(cat, 0) for cat in categories]
            # STYLING CHANGE: Updated colors to blue/red/grey palette
            bar_colors = ['#69dbf0', '#25acc4', '#14515c']

            if any(v > 0 for v in values):
                bars = ax2.bar(categories, values, color=bar_colors)
                # STYLING CHANGE: Updated text/tick/spine colors to dark/grey
                ax2.set_ylabel("Number of Patients", color='#333333', fontweight='bold')
                ax2.tick_params(axis='x', colors='#333333')
                ax2.tick_params(axis='y', colors='#333333')
                ax2.spines['bottom'].set_color('#CED4DA')
                ax2.spines['left'].set_color('#CED4DA')
                ax2.spines['top'].set_visible(False)
                ax2.spines['right'].set_visible(False)
                ax2.bar_label(bars, color='#333333', padding=3)
            else:
                # STYLING CHANGE: Updated text color to dark
                ax2.text(0.5, 0.5, 'No Adherence Data', transform=ax2.transAxes,
                         horizontalalignment='center',
                         verticalalignment='center',
                         color='#333333')
                ax2.axis('off')
        else:
            # STYLING CHANGE: Updated text color to dark
            ax2.text(0.5, 0.5, 'No Call Records Found', transform=ax2.transAxes,
                     horizontalalignment='center',
                     verticalalignment='center',
                     color='#333333')
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
        "<p style='text-align:center;color:#007BFF;font-size:14px;'>© 2025 CareLoop.AI | Empowering Connected Healthcare</p>",
        unsafe_allow_html=True
    )

elif menu == "Patient List":
    st.subheader("📋 Patient List")

    try:
        response = requests.get(f"{API_URL}/patient")
        response.raise_for_status()
        patients = response.json()


    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching patient data: {e}")
        patients = []
    except json.JSONDecodeError:
        st.error("Error decoding patient data from API.")
        patients = []
    if not patients:
        st.info("No patients found.")
    else:
        PAGE_SIZE = 5
        total_patients = len(patients)
        total_pages = math.ceil(total_patients / PAGE_SIZE)
        current_page = st.session_state.patient_list_page
        if current_page >= total_pages:  # Adjust if page is out of bounds (e.g., after deletion)
            current_page = max(0, total_pages - 1)
            st.session_state.patient_list_page = current_page
        start_index = current_page * PAGE_SIZE
        end_index = min(start_index + PAGE_SIZE, total_patients)  # Use min to avoid out-of-bounds
        patients_to_display = patients[start_index:end_index]  # Get the slice for the current page


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

        if not patients_to_display and total_patients > 0:
            st.warning(f"No patients to display on this page. Resetting to page 1.")
            st.session_state.patient_list_page = 0
            st.rerun()

        for patient in patients_to_display:
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

        st.markdown("---")
        nav_cols = st.columns([1, 2, 1])

        with nav_cols[0]:
            if st.button("⬅️ Previous", use_container_width=True, disabled=(current_page == 0)):
                st.session_state.patient_list_page -= 1
                st.rerun()

        with nav_cols[1]:
            st.markdown(
                f"<p style='text-align: center; color: #333; font-weight: 500;'>Page {current_page + 1} of {total_pages}</p>",unsafe_allow_html=True)

        with nav_cols[2]:
            if st.button("Next ➡️", use_container_width=True, disabled=(current_page >= total_pages - 1)):
                st.session_state.patient_list_page += 1
                st.rerun()

        if st.session_state.edit_patient_id:
            st.markdown("---")
            patient_to_edit = next(
                    (p for p in patients if p["_id"] == st.session_state.edit_patient_id),
                    None)
            if patient_to_edit:
                with st.form(f"edit_form_{patient_to_edit['_id']}"):
                    st.subheader(f"✏️ Edit Details for {patient_to_edit['name']}")
                    name = st.text_input("Name", value=patient_to_edit["name"])
                    age = st.number_input("Age", min_value=0, max_value=120, value=patient_to_edit["age"])
                    gender = st.selectbox("Gender", ["Male", "Female"],index=0 if patient_to_edit["gender"] == "Male" else 1)
                    phone = st.text_input("Phone", value=patient_to_edit["phone"])
                    disease = st.text_input("Disease", value=patient_to_edit["disease"])
                    try:
                        visit_date_default = datetime.strptime(patient_to_edit["visit_date"], "%Y-%m-%d").date()
                    except:
                        visit_date_default = date.today()
                    visit_date = st.date_input("Visit Date", value=visit_date_default)
                    prescribed_medication = st.text_area("Prescribed Medication (comma-separated)",value=", ".join(patient_to_edit["prescribed_medication"]))
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

elif menu == "Start Patient Follow-Up":
    st.subheader("📞 Start Patient Follow-Up")

    # --- POLLING, TIMEOUT, AND UI LOGIC ---
    if "monitoring_call_patient_name" in st.session_state:
        patient_name = st.session_state.monitoring_call_patient_name
        initial_count = st.session_state.initial_call_count
        start_time = st.session_state.monitoring_start_time

        # --- 1. TIMEOUT CHECK (NEW) ---
        # Check if 3 minutes (180s) have passed without completion
        if (time.time() - start_time) > 180:
            st.error(
                f"Call monitor timed out for {patient_name}. The call may have failed or was not answered. Resetting.")
            # Clear state and reset
            del st.session_state.monitoring_call_patient_name
            del st.session_state.initial_call_count
            del st.session_state.monitoring_start_time
            time.sleep(3)  # Give user time to read error
            st.rerun()

        # --- 2. POLLING CONTAINER (UPDATED) ---
        else:
            # This spinner now shows your custom container *inside* it
            with st.spinner("Monitoring call status..."):

                # --- This is the new UI container you asked for ---
                st.markdown(f"""
                <div class="call-status-container">
                    <div class="call-status-icons">
                        <span>🤖</span>
                        <span style="color: #007BFF; font-weight: 800;">... 📞 ...</span>
                        <span>🧑</span>
                    </div>
                    <div class="call-status-text">
                        AI call in progress with {patient_name}
                    </div>
                    <div class="call-status-subtext">
                        Checking for call completion. This may take a moment.
                    </div>
                </div>
                """, unsafe_allow_html=True)
                # --- End of new UI container ---

                time.sleep(10)  # Poll every 10 seconds

                try:
                    records_res = requests.get(f"{API_URL}/patient/call-records")
                    if records_res.status_code == 200:
                        current_count = len(records_res.json())

                        # Check if a new record has been added
                        if current_count > initial_count:
                            st.success(f"✅ Call with {patient_name} has ended.")
                            st.balloons()
                            del st.session_state.monitoring_call_patient_name
                            del st.session_state.initial_call_count
                            del st.session_state.monitoring_start_time
                            st.rerun()
                        else:
                            st.rerun()  # Keep polling
                    else:
                        st.error("Error checking call status. Stopping monitor.")
                        del st.session_state.monitoring_call_patient_name
                        del st.session_state.initial_call_count
                        del st.session_state.monitoring_start_time
                        st.rerun()
                except Exception as e:
                    st.error(f"Connection error: {e}. Stopping monitor.")
                    del st.session_state.monitoring_call_patient_name
                    del st.session_state.initial_call_count
                    del st.session_state.monitoring_start_time
                    st.rerun()

    # --- "START CALL" PAGE LOGIC (IF NOT MONITORING) ---
    elif "monitoring_call_patient_name" not in st.session_state:
        try:
            res = requests.get(f"{API_URL}/patient/pending-followup-patients")
            if res.status_code != 200:
                st.error("Could not fetch pending patients.")
                st.stop()
            patients = res.json()
        except Exception as e:
            st.error(f"Error connecting to API: {e}")
            st.stop()

        name_pres = [pat["name"] for pat in patients if "name" in pat]
        if name_pres:
            options = ["-- Select a patient --"] + name_pres
            sel_name = st.selectbox("Select Patient Name", options, key="patient_select")

            if sel_name != "-- Select a patient --":
                pati = next((p for p in patients if p["name"] == sel_name), None)
                if pati:
                    st.markdown("---")
                    with st.container():
                        st.write("### 📋 Selected Patient Details:")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Name:** {pati['name']}")
                            st.write(f"**Age:** {pati['age']}")
                            st.write(f"**Gender:** {pati['gender']}")
                        with col2:
                            st.write(f"**Phone:** {pati['phone']}")
                            st.write(f"**Visit Date:** {pati['visit_date']}")
                        st.write(f"**Prescribed Medication:** {', '.join(pati['prescribed_medication'])}")
                    st.markdown("---")

                    if st.button("📞 Start Patient Follow-Up"):
                        try:
                            initial_records_res = requests.get(f"{API_URL}/patient/call-records")
                            if initial_records_res.status_code == 200:
                                initial_count = len(initial_records_res.json())
                            else:
                                st.error("Could not get initial call count. Aborting.")
                                st.stop()

                            call_data = {"patient_id": pati["_id"], "name": pati["name"], "phone": pati["phone"]}
                            call_res = requests.post(f"{CALL_API_URL}/patient/call_number", json=call_data)

                            if call_res.status_code == 200:
                                # --- SET ALL MONITORING STATES ---
                                st.session_state.monitoring_call_patient_name = pati["name"]
                                st.session_state.initial_call_count = initial_count
                                st.session_state.monitoring_start_time = time.time()  # <-- ADDED TIMEOUT

                                st.info(f"Initiating AI call to {pati['name']}... Monitoring for completion.")
                                time.sleep(2)
                                st.rerun()
                            else:
                                st.error("Failed to initiate call. Please check backend logs.")
                        except Exception as e:
                            st.error(f"Error connecting to backend: {e}")
            else:
                st.info("👆 Please select a patient from the dropdown to view details and start follow-up.")
        else:
            st.info("No patients are currently pending follow-up.")

elif menu == "Patient Feedback":

    st.subheader("💬 Patient Feedback Summary")

    if "selected_call_record" in st.session_state and st.session_state.selected_call_record is not None:
        record = st.session_state.selected_call_record
        patient_name = record.get('patient_name', 'Unknown Patient')
        call_date = record.get('start_time', '').split('T')[0]

        st.markdown(f"### Chat History for {patient_name}")
        st.markdown(f"**Call Date:** {call_date}")

        st.markdown("#### Call Summary:")
        col1_sum, col2_sum, col3_sum = st.columns(3)

        sentiment = record.get('overall_sentiment', 'UNCLEAR')
        sentiment_emoji = get_sentiment_emoji(sentiment)
        with col1_sum:
            st.metric(label="Overall Sentiment", value=f"{sentiment_emoji} {sentiment}")

        adherence = record.get('medical_adherence', 'UNCLEAR')
        adherence_emoji = get_adherence_emoji(adherence)
        with col2_sum:
            st.metric(label="Medication Adherence", value=f"{adherence_emoji} {adherence}")

        side_effects = record.get('side_effects_reported', False)
        side_effects_display = get_side_effects_display(side_effects)
        with col3_sum:
            st.metric(label="Side Effects", value=side_effects_display)

        st.markdown("---")

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
                        cols[2].markdown("**Sentiment**")
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
                            record_id = record.get('_id', record.get('id'))
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
                    st.divider()
                    header_cols = st.columns(column_weights)
                    for i, header in enumerate(column_headers):
                        header_cols[i].markdown(f"**{header}**")
                    st.divider()

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
                    st.divider()
                    header_cols = st.columns(column_weights)
                    for i, header in enumerate(column_headers):
                        header_cols[i].markdown(f"**{header}**")
                    st.divider()

                    for appt in past_appointments:
                        cols = st.columns(column_weights)
                        cols[0].write(appt.get('patient_name', 'N/A'))
                        cols[1].write(appt.get('department', 'N/A'))
                        cols[2].write(appt.get('appointment_date', 'N/A'))
                        cols[3].write(appt.get('appointment_time', 'N/A'))
                        status = appt.get('status', 'N/A')
                        if status == "Visited":
                            cols[4].markdown(f"✔️ {status}")
                        else:
                            cols[4].write(status)
            else:
                st.error(f"Failed to fetch past appointments: {res.text}")
        except Exception as e:
            st.error(f"Error fetching past appointments: {e}")


elif menu == "Analytics":
    # This section duplicates the Dashboard.
    # In a production app, you'd factor this into a shared function.
    # For this refactor, I will apply the same styling changes here.

    st.subheader("📊 Key Metrics")
    total_patients = "N/A"
    total_engaged = "N/A"
    total_alerts = "N/A"

    try:
        patients_res = requests.get(f"{API_URL}/patient")
        if patients_res.status_code == 200:
            total_patients = len(patients_res.json())
        metrics_res = requests.get(f"{API_URL}/patient/metrics")
        if metrics_res.status_code == 200:
            metrics_data = metrics_res.json()
            total_engaged = metrics_data.get('total_patients_engaged', 0)
            total_alerts = metrics_data.get('total_flagged_alerts', 0)
    except Exception as e:
        st.error(f"Error connecting to API: {e}")

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
        st.markdown(
            f"""
                <div class="metric-card">
                    <img src="https://cdn-icons-png.flaticon.com/512/455/455705.png" width="60">
                    <div class="metric-label">Patients Engaged</div>
                    <div class="metric-value">{total_engaged}</div>
                </div>
                """, unsafe_allow_html=True)
    with col3:
        st.markdown(
            f"""
                <div class="metric-card">
                    <img src="https://cdn-icons-png.flaticon.com/512/7249/7249210.png" width="60">
                    <div class="metric-label">Active Alerts</div>
                    <div class="metric-value">{total_alerts}</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<h3 style="color: #007BFF; margin-top: 40px;">📈 Insights Overview</h3>', unsafe_allow_html=True)

    call_records = []
    try:
        records_res = requests.get(f"{API_URL}/patient/call-records")
        if records_res.status_code == 200:
            call_records = records_res.json()
    except Exception as e:
        st.error(f"Error connecting to API for call records: {e}")



    col_left, col_right = st.columns(2)

    # 1. Sentiment Pie Chart
    with col_left:
        st.subheader("Follow-up Sentiment")
        # STYLING CHANGE: Updated facecolor to white
        fig1, ax1 = plt.subplots(facecolor='#FFFFFF')
        ax1.set_facecolor('#FFFFFF')

        if call_records:
            sentiments = [record.get('overall_sentiment', 'NEUTRAL') for record in call_records]
            sentiment_counts = Counter(sentiments)
            labels = ["POSITIVE", "NEUTRAL", "ALERT"]
            sizes = [sentiment_counts.get(label, 0) for label in labels]
            # STYLING CHANGE: Updated colors to blue/grey/red palette
            colors = ['#69dbf0', '#25acc4', '#14515c']

            non_zero_labels = [label for i, label in enumerate(labels) if sizes[i] > 0]
            non_zero_sizes = [size for size in sizes if size > 0]
            non_zero_colors = [color for i, color in enumerate(colors) if sizes[i] > 0]

            if non_zero_sizes:
                ax1.pie(non_zero_sizes, labels=non_zero_labels, autopct='%1.1f%%', startangle=90,
                        colors=non_zero_colors,
                        # STYLING CHANGE: Updated text color to dark
                        textprops={'color': '#333333', 'fontsize': 12, 'weight': 'bold'})
                ax1.axis('equal')
            else:
                # STYLING CHANGE: Updated text color to dark
                ax1.text(0.5, 0.5, 'No Sentiment Data', horizontalalignment='center', verticalalignment='center',
                         color='#333333')
                ax1.axis('off')
        else:
            # STYLING CHANGE: Updated text color to dark
            ax1.text(0.5, 0.5, 'No Call Records Found', horizontalalignment='center', verticalalignment='center',
                     color='#333333')
            ax1.axis('off')

        st.pyplot(fig1)

    # 2. Adherence Bar Chart
    with col_right:
        st.subheader("Medication Adherence")
        # STYLING CHANGE: Updated facecolor to white
        fig2, ax2 = plt.subplots(facecolor='#FFFFFF')
        ax2.set_facecolor('#FFFFFF')

        if call_records:
            adherence_statuses_raw = [
                record.get('medical_adherence', 'NOT_ASKED')
                for record in call_records
            ]
            adherence_statuses = [
                "UNCLEAR" if status == "NOT_ASKED" else status
                for status in adherence_statuses_raw
            ]
            adherence_counts = Counter(adherence_statuses)

            categories = ["ADHERENT", "NON-ADHERENT", "UNCLEAR"]
            values = [adherence_counts.get(cat, 0) for cat in categories]
            # STYLING CHANGE: Updated colors to blue/red/grey palette
            bar_colors = ['#69dbf0', '#25acc4', '#14515c']

            if any(v > 0 for v in values):
                bars = ax2.bar(categories, values, color=bar_colors)
                # STYLING CHANGE: Updated text/tick/spine colors to dark/grey
                ax2.set_ylabel("Number of Patients", color='#333333', fontweight='bold')
                ax2.tick_params(axis='x', colors='#333333')
                ax2.tick_params(axis='y', colors='#333333')
                ax2.spines['bottom'].set_color('#CED4DA')
                ax2.spines['left'].set_color('#CED4DA')
                ax2.spines['top'].set_visible(False)
                ax2.spines['right'].set_visible(False)
                ax2.bar_label(bars, color='#333333', padding=3)
            else:
                # STYLING CHANGE: Updated text color to dark
                ax2.text(0.5, 0.5, 'No Adherence Data', transform=ax2.transAxes,
                         horizontalalignment='center',
                         verticalalignment='center',
                         color='#333333')
                ax2.axis('off')
        else:
            # STYLING CHANGE: Updated text color to dark
            ax2.text(0.5, 0.5, 'No Call Records Found', transform=ax2.transAxes,
                     horizontalalignment='center',
                     verticalalignment='center',
                     color='#333333')
            ax2.axis('off')

        st.pyplot(fig2)

    st.markdown("---")
    if st.button("🔬 Run Root Cause Analysis on Negative Calls"):
        with st.spinner("Analyzing negative call records... This may take a moment."):
            try:
                res = requests.post(f"{API_URL}/patient/run-root-cause-analysis")
                if res.status_code == 200:
                    st.success(res.json().get("message", "Analysis complete!"))
                else:
                    st.error(f"Analysis failed: {res.text}")
            except Exception as e:
                st.error(f"Error connecting to analysis API: {e}")

    root_cause_data = {}
    try:
        rca_res = requests.get(f"{API_URL}/patient/negative-experience-drivers")
        if rca_res.status_code == 200:
            root_cause_data = rca_res.json()
    except Exception as e:
        st.error(f"Error connecting to API for root cause data: {e}")

    col_rca, col_non_rca = st.columns(2)
    with col_rca:
        st.subheader("Top Drivers of Negative Experience")
        fig_rca, ax_rca = plt.subplots(facecolor='white')
        ax_rca.set_facecolor('white')

        if root_cause_data:
            sorted_data = sorted(root_cause_data.items(), key=lambda item: item[1], reverse=True)
            labels = [item[0] for item in sorted_data]
            sizes = [item[1] for item in sorted_data]
            colors = plt.cm.Blues_r([x / len(labels) for x in range(len(labels))])  # Your blue theme

            if any(s > 0 for s in sizes):
                bars = ax_rca.barh(labels, sizes, color=colors)
                # Fix label/tick/spine colors for light theme
                ax_rca.set_xlabel("Number of Mentions", color='#333333', fontweight='bold')
                ax_rca.tick_params(axis='x', colors='#333333')
                ax_rca.tick_params(axis='y', colors='#333333')
                ax_rca.spines['bottom'].set_color('#CED4DA')
                ax_rca.spines['left'].set_color('#CED4DA')
                ax_rca.spines['top'].set_visible(False)
                ax_rca.spines['right'].set_visible(False)
                ax_rca.invert_yaxis()
                ax_rca.bar_label(bars, color='#333333', padding=5)  # Fix label color
            else:
                ax_rca.text(0.5, 0.5, 'No Negative Data Analyzed',
                            horizontalalignment='center', verticalalignment='center',
                            color='black', transform=ax_rca.transAxes)
                ax_rca.axis('off')
        else:
            ax_rca.text(0.5, 0.5, 'No Data Available or Analysis Not Run',
                        horizontalalignment='center', verticalalignment='center',
                        color='black', transform=ax_rca.transAxes)
            ax_rca.axis('off')
        st.pyplot(fig_rca)

    with col_non_rca:
        pass

elif menu == "Logout":
    st.session_state.clear()
    st.success("You have been logged out successfully.")
    time.sleep(1)
    st.switch_page("ui_file.py")