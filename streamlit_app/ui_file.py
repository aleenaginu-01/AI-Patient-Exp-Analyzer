import streamlit as st
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="CareLoop.ai - Healthcare Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide sidebar completely
st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    [data-testid="collapsedControl"] {display: none;}
</style>
""", unsafe_allow_html=True)

# Custom CSS for professional styling and animations
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    /* REFINED: Light, clinical background for the whole app */
    .stApp {
        background-color: #b9f0de;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}
    section[data-testid="stSidebar"] {display: none;}
    .css-1d391kg {display: none;}

    /* REFINED: Main container with softer shadow and light border */
    .main-container {
        background: #d4faf1;
        border-radius: 20px;
        padding: 40px;
        margin: 20px auto;
        max-width: 1200px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.05); /* Softer shadow */
        border: 1px solid #E9ECEF; /* Subtle border */
        animation: fadeInUp 0.8s ease-out;
    }

    /* Logo and Header */
    .logo-container {
        text-align: center;
        margin-bottom: 40px;
        animation: fadeIn 1s ease-in;
    }

    .logo {
        font-size: 48px;
        font-weight: 700;
        color:  #245444; /* Dark, legible title color */
        margin-bottom: 10px;
    }

    .tagline {
        color: #5A6A7B; /* Dark, legible subtitle color */
        font-size: 18px;
        font-weight: 400;
    }

    /* Stats Cards (Accent color used well) */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
        margin: 30px 0;
    }

    .stat-card {
        background: #d4faf1;
        border-radius: 15px;
        padding: 25px;
        color:  #245444;
        box-shadow: 0 10px 30px rgba(78, 195, 245, 0.25);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        animation: slideIn 0.6s ease-out;
    }

    .stat-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 40px rgba(78, 195, 245, 0.35);
    }

    .stat-number {
        font-size: 36px;
        font-weight: 700;
        margin: 10px 0;
        color:  #245444;
    }

    .stat-label {
        font-size: 14px;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Features Section */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 25px;
        margin-top: 40px;
    }

    /* REFINED: Feature card with clean border and shadow as requested */
    .feature-card {
        background: #d4faf1;
        border-radius: 15px;
        padding: 30px;
        border: 1px solid #E0E0E0; /* Requested subtle border */
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); /* Requested subtle shadow */
        transition: all 0.3s ease;
        animation: fadeInUp 0.8s ease-out;
    }

    /* REFINED: Hover state uses consistent accent color */
    .feature-card:hover {
        border-color:  #245444; /* Use primary accent color */
        box-shadow: 0 6px 16px rgba(78, 195, 245, 0.15); /* Accent shadow */
        transform: translateY(-5px);
    }

    .feature-icon {
        font-size: 40px;
        margin-bottom: 15px;
    }

    .feature-title {
        font-size: 20px;
        font-weight: 600;
        color:  #245444; /* Dark, legible */
        margin-bottom: 10px;
    }

    .feature-desc {
        color:  #245444; /* Dark, legible */
        font-size: 14px;
        line-height: 1.6;
    }

    /* --- LOGIN FORM STYLES --- */
    /* REFINED: Softer shadow and cleaner border */
    # .login-container {
    #     max-width: 480px;
    #     margin: 50px auto;
    #     background: #FFFFFF;
    #     border-radius: 24px;
    #     padding: 50px 45px;
    #     box-shadow: 0 10px 40px rgba(0, 0, 0, 0.06); /* Softer shadow */
    #     border: 1px solid #E9ECEF; /* Cleaner border */
    #     animation: fadeInUp 0.6s ease-out;
    #     display: flex;
    #     flex-direction: column;
    #     align-items: center;
    # }

    .login-header {
        text-align: center;
        margin-bottom: 40px;
    }

    .login-title {
        font-size: 32px;
        font-weight: 700;
        color: #1A2B4D;
        margin-bottom: 8px;
    }

    .login-subtitle {
        color: #5A6A7B;
        font-size: 15px;
        font-weight: 400;
        margin-top: 10px;
    }

    /* LIGHT INPUT FIELDS - Professional Healthcare Theme (Already excellent) */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        background-color: white !important;
        border: 1.5px solid #E1E8ED !important;
        border-radius: 12px !important;
        padding: 14px 18px !important;
        font-size: 15px !important;
        color: black !important; /* Dark, legible input text */
        transition: all 0.3s ease !important;
        font-weight: 400 !important;
        max-width: 400px !important;
        margin: 0 auto !important;
    }

    /* Center input containers and labels */
    .stTextInput, .stSelectbox {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
    }

    .stTextInput > div, .stSelectbox > div {
        width: 100% !important;
        max-width: 400px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
    }

    .stTextInput > label, .stSelectbox > label {
        width: 400px !important;
        max-width: 400px !important;
    }

    /* Focus state uses accent color */
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        background-color: #FFFFFF !important;
        border-color: #4ec3f5 !important;
        box-shadow: 0 0 0 3px rgba(78, 195, 245, 0.1) !important;
        outline: none !important;
    }

    .stTextInput > div > div > input::placeholder {
        color: #A0AEC0 !important;
        font-weight: 300 !important;
    }

    /* Dropdown styling - WHITE background */
    .stSelectbox > div > div > select {
        cursor: pointer !important;
        appearance: none !important;
        background-color: #FFFFFF !important;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23A0AEC0' d='M6 9L1 4h10z'/%3E%3C/svg%3E") !important;
        background-repeat: no-repeat !important;
        background-position: right 16px center !important;
        padding-right: 45px !important;
    }

    /* Light dropdown options */
    .stSelectbox > div > div > select option {
        background-color: #FFFFFF !important;
        color: #2C3E50 !important;
    }

    .stSelectbox > div > div > select:hover {
        border-color: #4ec3f5 !important;
        background-color: #FFFFFF !important;
    }

    /* Label styling (Dark and legible) */
    .stTextInput > label,
    .stSelectbox > label {
        color: #2C3E50 !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        margin-bottom: 8px !important;
        letter-spacing: 0.2px !important;
        text-align: center !important;
        width: 100% !important;
    }

    /* --------------------------------- */
    /* --- BUTTON STYLES (CLEANED) --- */
    /* --------------------------------- */

    /* General Button Style (Primary) */
    .stButton > button {
        width: 100%; /* Works with use_container_width=True */
        background: linear-gradient(135deg, #8debd2 0%, #62b59f 100%);
        color: black;
        border: none;
        padding: 16px 30px;
        font-size: 16px;
        font-weight: 600;
        border-radius: 12px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(78, 195, 245, 0.3);
        letter-spacing: 0.3px;
    }
    
    .patient-login-button .stButton > button {
        width: 100%; /* Works with use_container_width=True */
        background: linear-gradient(135deg, #8debd2 0%, #62b59f 100%);
        color: black;
        border: none;
        padding:18px 40px;
        font-size: 16px;
        font-weight: 600;
        border-radius: 12px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(78, 195, 245, 0.3);
        letter-spacing: 0.3px;
    }
    
    
    .patient-login-button {
        width: 100%;
        max-width: 400px;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #1c8065 0%, #62b59f 100%);
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(78, 195, 245, 0.4);
    }

    .stButton > button:active {
        transform: translateY(0px);
    }

    /* Login to Portal button on dashboard (Slightly larger) */
    .stButton > button:contains('Login to Portal') {
        background: linear-gradient(135deg, #8debd2 0%, #62b59f 100%);
        font-size: 17px;
        padding: 18px 40px;
        box-shadow: 0 8px 25px rgba(78, 195, 245, 0.35);
    }

    /* --- SPECIFIC BUTTON CLASSES (Unchanged, already correct) --- */

    /* Admin Login Button (in col1) - Inherits default blue style */
    .admin-login-button .stButton > button {
        /* No override needed, it takes the main primary style */
    }

    /* Admin Back Button (in col2) - Secondary/Ghost style */
    .admin-back-button .stButton > button {
        background: #FFFFFF;
        color: #5A6A7B; /* Dark, legible text */
        border: 1.5px solid #E1E8ED; /* Light grey border */
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }

    .admin-back-button .stButton > button:hover {
        background: #F8FAFB;
        color: #2C3E50;
        border-color: #CBD5E0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }

    /* Patient Login Button - Inherits primary style, width handled by default */
    .patient-login-button .stButton > button {
        /* This rule is intentionally blank, it correctly
           inherits the main .stButton > button style (width: 100%)
           which is what we want.
        */
    }

    /* --------------------------------- */
    /* --- END OF BUTTON STYLES --- */
    /* --------------------------------- */


    /* Success and error messages */
    .stSuccess, .stError, .stWarning {
        border-radius: 12px !important;
        padding: 14px 18px !important;
        margin-top: 16px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
    }

    .stSuccess {
        background-color: #036b4f !important;
        color: white !important;
        border: 1px solid #C3E6CB !important;
    }

    .stError {
        background-color: #F8D7DA !important;
        color: #721C24 !important;
        border: 1px solid #F5C6CB !important;
    }

    .stWarning {
        background-color: #e8bf3f !important;
        color: black !important;
        border: 1px solid #FFEAA7 !important;
    }

    /* Spinner */
    .stSpinner > div {
        border-color: #4ec3f5 !important;
    }

    /* Animations */
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False


def show_dashboard():
    # Logo and Header
    st.markdown("""
    <div class="main-container">
        <div class="logo-container">
            <div class="logo">🏥 CareLoop.ai</div>
            <div class="tagline">Intelligent Healthcare Management System</div>
        </div>
    """, unsafe_allow_html=True)

    # Stats Section
    st.markdown("""
    <div class="stats-container">
        <div class="stat-card">
            <div class="stat-label">Total Departments</div>
            <div class="stat-number">35</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Today's Appointments</div>
            <div class="stat-number">16</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Available Doctors</div>
            <div class="stat-number">97</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Bed Occupancy</div>
            <div class="stat-number">78%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Login Button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔐 Login to Portal", use_container_width=True):
            st.session_state.page = 'login'
            st.rerun()

    # Features Section
    st.markdown("""
    <div class="features-grid">
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Real-time Analytics</div>
            <div class="feature-desc">Monitor hospital operations with live data visualization and comprehensive reporting tools.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">👨‍⚕️</div>
            <div class="feature-title">Patient Management</div>
            <div class="feature-desc">Streamlined patient records, appointment scheduling, and medical history tracking.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">💊</div>
            <div class="feature-title">Prescription System</div>
            <div class="feature-desc">Digital prescription management with automated refill reminders and drug interaction alerts.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🔔</div>
            <div class="feature-title">Smart Notifications</div>
            <div class="feature-desc">Automated alerts for appointments, medication schedules, and critical patient updates.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🔒</div>
            <div class="feature-title">Secure & Compliant</div>
            <div class="feature-desc">HIPAA-compliant security with encrypted data storage and secure access controls.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <div class="feature-title">AI-Powered Insights</div>
            <div class="feature-desc">Machine learning algorithms for predictive analytics and intelligent decision support.</div>
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)


def show_login():
    st.markdown("""
    <div class="login-container">
        <div class="login-header">
            <div class="login-title">🏥 CareLoop.ai</div>
            <p class="login-subtitle">Sign in to your account</p>
        </div>
    """, unsafe_allow_html=True)

    # Role Selection
    role = st.selectbox(
        "Select Your Role",
        ["Patient", "Admin"],
        index=0
    )

    if role == "Admin":
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")

        col1, col2 = st.columns(2)

        with col1:
            # Wrap Login button in its CSS class
            st.markdown('<div class="admin-login-button">', unsafe_allow_html=True)
            if st.button("Login", use_container_width=True):
                if username == "admin" and password == "1234":
                    with st.spinner("Authenticating..."):
                        time.sleep(1)
                        st.session_state.logged_in = True
                        st.session_state.user_role = role
                        st.success(f"✅ Welcome, Admin!")
                        time.sleep(1)
                        st.switch_page("pages/dashboard.py")
                else:
                    st.error("Incorrect username or password")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            # Wrap Back button in its CSS class
            st.markdown('<div class="admin-back-button">', unsafe_allow_html=True)
            if st.button("Back to Dashboard", use_container_width=True):
                st.session_state.page = 'dashboard'
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    elif role == "Patient":
        patient_id = st.text_input("Enter Patient ID or Phone Number", placeholder="e.g., LIS123")

        # Wrap Patient Login button in its CSS class
        st.markdown('<div class="patient-login-button">', unsafe_allow_html=True)
        if st.button("Login as Patient"):
            if patient_id.strip() == "LIS123":
                st.success("Welcome! Redirecting to your User Page...")
                st.session_state["user_role"] = "patient"
                st.session_state["patient_id"] = patient_id
                st.switch_page("pages/user.py")
            else:
                st.warning("Please enter your Patient ID or Phone Number.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Additional Info
    st.markdown("""
    <div style="text-align: center; margin-top: 30px; color: #5A6A7B;">
        <p style="font-size: 14px;">Don't have an account? <a href="#" style="color: #4ec3f5; font-weight: 600; text-decoration: none;">Contact Administrator</a></p>
        <p style="font-size: 12px; margin-top: 10px; opacity: 0.7;">© 2024 CareLoop.ai - All rights reserved</p>
    </div>
    """, unsafe_allow_html=True)


# Main App Logic
if st.session_state.page == 'dashboard':
    show_dashboard()
elif st.session_state.page == 'login':
    show_login()