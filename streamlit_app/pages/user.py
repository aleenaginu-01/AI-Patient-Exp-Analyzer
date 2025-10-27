import streamlit as st

st.set_page_config(page_title="Patient Dashboard", layout="wide")

# Enhanced CSS with professional styling (matching admin dashboard)
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

        /* Input Fields */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div,
        .stTextArea textarea {
            background: rgba(20, 184, 166, 0.05) !important;
            border: 1px solid #14b8a6 !important;
            border-radius: 8px !important;
            color: #e8f5f7 !important;
            padding: 10px !important;
        }

        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus,
        .stSelectbox > div > div:focus-within,
        .stTextArea textarea:focus {
            border: 2px solid #06b6d4 !important;
            box-shadow: 0 0 10px rgba(20, 184, 166, 0.3) !important;
        }

        /* Labels */
        .stTextInput > label,
        .stNumberInput > label,
        .stSelectbox > label,
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

        /* Welcome message styling */
        .welcome-message {
            background: linear-gradient(135deg, rgba(20, 184, 166, 0.1) 0%, rgba(6, 182, 212, 0.1) 100%);
            border: 1px solid rgba(20, 184, 166, 0.3);
            border-radius: 15px;
            padding: 20px 30px;
            margin: 20px 0;
            text-align: center;
            animation: fadeIn 0.8s ease;
        }

        .welcome-message p {
            color: #e8f5f7 !important;
            font-size: 18px !important;
            font-weight: 500 !important;
        }

        /* Info cards for patient dashboard */
        .info-card {
            background: linear-gradient(135deg, rgba(20, 184, 166, 0.1) 0%, rgba(6, 182, 212, 0.05) 100%);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(20, 184, 166, 0.3);
            transition: all 0.4s ease;
            animation: fadeIn 0.8s ease;
            margin: 20px 0;
        }

        .info-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 35px rgba(20, 184, 166, 0.4);
            border-color: #14b8a6;
        }

        .info-card h4 {
            color: #14b8a6 !important;
            font-size: 22px !important;
            font-weight: 600 !important;
            margin-bottom: 15px !important;
        }

        .info-card p {
            color: #a7f3d0 !important;
            font-size: 15px !important;
            line-height: 1.8 !important;
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

# Welcome message with custom styling
st.markdown(f"""
    <div class="welcome-message">
        <p>Welcome, Patient <strong>{patient_id}</strong>! 👋</p>
    </div>
""", unsafe_allow_html=True)

if menu == "My Feedback":
    st.subheader("💬 My Feedback History")
    st.markdown("""
        <div class="info-card">
            <h4>📋 Recent Feedback</h4>
            <p>Your feedback helps us improve our care. View your previous responses and communication history here.</p>
        </div>
    """, unsafe_allow_html=True)
    st.info("Your feedback history will appear here.")

elif menu == "Medication Status":
    st.subheader("💊 Medication Tracking")
    st.markdown("""
        <div class="info-card">
            <h4>✅ Medication Compliance</h4>
            <p>Stay on track with your prescribed medications. Check your schedule and mark your daily doses.</p>
        </div>
    """, unsafe_allow_html=True)
    st.success("No pending medication reminders.")

elif menu == "View Appointments":
    st.subheader("📅 My Appointments")
    st.markdown("""
        <div class="info-card">
            <h4>🗓️ Upcoming Visits</h4>
            <p>View and manage your scheduled appointments with your healthcare provider.</p>
        </div>
    """, unsafe_allow_html=True)
    st.info("No Appointments Scheduled")

elif menu == "Logout":
    st.session_state.clear()
    st.success("You have been logged out successfully.")
    st.switch_page("ui_file.py")