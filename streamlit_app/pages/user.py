import streamlit as st

st.set_page_config(page_title="Patient Dashboard", layout="wide")

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

        /* --- LIGHT THEME INPUTS --- */
        /* ... (All .stTextInput, .stSelectbox, .stDateInput styles from dashboard.py) ... */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stTextArea textarea {
            background-color: #FFFFFF !important;
            border: 1.5px solid #CED4DA !important;
            /* ... etc ... */
        }
        .stSelectbox div[data-baseweb="select"] {
            background: #FFFFFF !important;
            /* ... etc ... */
        }
        .stDateInput input {
            background: #FFFFFF !important;
            /* ... etc ... */
        }
        .stTextInput > label,
        .stNumberInput > label,
        .stSelectbox > label,
        .stDateInput > label,
        .stTextArea > label {
            color: #1A2B4D !important;
            font-weight: 500 !important;
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

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] { gap: 8px; }
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
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Custom metric cards */
        .metric-card {
            background: #FFFFFF;
            border: 1px solid #E0E0E0;
            color: #245444;
            /* ... (rest of .metric-card styles from dashboard.py) ... */
        }
        .metric-label {
            color: #245444;
            /* ... (rest of .metric-label styles) ... */
        }
        .metric-value {
            color: #245444;
            /* ... (rest of .metric-value styles) ... */
        }

        /* Chat box styling */
        .chat-box {
            background: #F8F9FA;
            /* ... (rest of .chat-box styles) ... */
        }
        .message { /* ... */ }
        .ai { /* ... */ }
        .user { /* ... */ }

        /* Vision/Mission cards (This is what we will reuse) */
        .vision-card {
            background: #FFFFFF;
            padding: 30px;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            border: 1px solid #E0E0E0;
            transition: all 0.4s ease;
            animation: fadeIn 0.8s ease;
            height: 100%;
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

        /* Metric styling for chat page */
        [data-testid="stMetric"] {
            background-color: #FFFFFF;
            border: 1px solid #E0E0E0;
            /* ... (rest of stMetric styles) ... */
        }
        [data-testid="stMetricLabel"] {
            color: #5A6A7B !important;
            /* ... (rest of stMetricLabel styles) ... */
        }
        [data-testid="stMetricValue"] {
            color: #1A2B4D !important;
            /* ... (rest of stMetricValue styles) ... */
        }
    </style>
"""
st.markdown(hide_default_format, unsafe_allow_html=True)

# Header
st.title("🏥 CareLoop.AI - Patient Portal")

st.sidebar.title("Patient Panel")

menu = st.sidebar.radio(
    "Select View:",
    ["My Feedback", "Medication Status", "View Appointments", "Logout"],
    label_visibility="visible",
)

st.sidebar.divider()

patient_id = st.session_state.get("patient_id", "Guest")

# --- (2) MODIFICATION: Replaced .welcome-message with st.info ---
# This will automatically adopt the light theme's .stInfo style
st.info(f"**Welcome, Patient {patient_id}!** 👋")

if menu == "My Feedback":
    st.subheader("💬 My Feedback History")

    # --- (3) MODIFICATION: Replaced .info-card with .vision-card ---
    st.markdown("""
        <div class="vision-card">
            <h4>📋 Recent Feedback</h4>
            <p>Your feedback helps us improve our care. View your previous responses and communication history here.</p>
        </div>
    """, unsafe_allow_html=True)
    # --- END MODIFICATION ---

    st.info("Your feedback history will appear here.")

elif menu == "Medication Status":
    st.subheader("💊 Medication Tracking")

    # --- (3) MODIFICATION: Replaced .info-card with .vision-card ---
    st.markdown("""
        <div class="vision-card">
            <h4>✅ Medication Compliance</h4>
            <p>Stay on track with your prescribed medications. Check your schedule and mark your daily doses.</p>
        </div>
    """, unsafe_allow_html=True)
    # --- END MODIFICATION ---

    st.success("No pending medication reminders.")

elif menu == "View Appointments":
    st.subheader("📅 My Appointments")

    # --- (3) MODIFICATION: Replaced .info-card with .vision-card ---
    st.markdown("""
        <div class="vision-card">
            <h4>🗓️ Upcoming Visits</h4>
            <p>View and manage your scheduled appointments with your healthcare provider.</p>
        </div>
    """, unsafe_allow_html=True)
    # --- END MODIFICATION ---

    st.info("No Appointments Scheduled")

elif menu == "Logout":
    st.session_state.clear()
    st.success("You have been logged out successfully.")
    st.switch_page("ui_file.py")