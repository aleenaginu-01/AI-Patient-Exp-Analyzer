import streamlit as st
import time
from datetime import datetime
if st.session_state.get("logged_in"):
    st.switch_page("pages/dashboard.py")
    st.stop()
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
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.05);
        border: 1px solid #E9ECEF;
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
        color:  #245444;
        margin-bottom: 10px;
    }

    .tagline {
        color: #5A6A7B;
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
        border: 1px solid #E0E0E0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
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

    /* --- STYLES FOR TEXT INPUTS (Light Theme) --- */
    .stTextInput > div > div > input,
    .stTextArea textarea { 
        background-color: white !important;
        border: 1.5px solid #E1E8ED !important;
        border-radius: 12px !important;
        padding: 14px 18px !important;
        font-size: 15px !important;
        color: black !important; /* Black text */
        transition: all 0.3s ease !important;
        font-weight: 400 !important;
        max-width: 400px !important;
        margin: 0 auto !important;
        caret-color: black !important;
    }

    /* Center input containers and labels */
    .stTextInput {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
    }
    .stTextInput > div {
        width: 100% !important;
        max-width: 400px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
    }
    .stTextInput > label {
        width: 400px !important;
        max-width: 400px !important;
    }

    /* Focus state for Text Input */
    .stTextInput > div > div > input:focus {
        background-color: #FFFFFF !important;
        border-color: #4ec3f5 !important;
        box-shadow: 0 0 0 3px rgba(78, 195, 245, 0.1) !important;
        outline: none !important;
    }

    /* Placeholder text */
    .stTextInput > div > div > input::placeholder {
        color: #A0AEC0 !important;
        font-weight: 300 !important;
    }

    /* Label styling */
    .stTextInput > label {
        color: #2C3E50 !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        margin-bottom: 8px !important;
        letter-spacing: 0.2px !important;
        text-align: center !important;
        width: 100% !important;
    }
    /* --- END OF INPUT STYLES --- */


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

    /* Admin Login Button (in col1) - Inherits primary style */
    .admin-login-button .stButton > button {
        /* No override needed */
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
        max-width: 400px; /* Center alerts */
        margin-left: auto;
        margin-right: auto;
    }

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

    [data-testid="stAlert"] * {
        color: #856404 !important; /* Fix for warning text color */
    }

    /* Spinner */
    .stSpinner > div {
        border-color: #4ec3f5 !important;
    }

    /* Animations */
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
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
            <div class="feature-icon">📊</div>
            <div class="feature-title">Real-time Analytics</div>
            <div class="feature-desc">Monitor hospital operations with live data visualization and comprehensive reporting tools.</div>
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)


def show_login():
    st.markdown("""
    <div class="login-container">
        <div class="login-header">
            <div class="login-title">🏥 CareLoop.ai</div>
            <p class="login-subtitle">Admin Sign In</p>
        </div>
    """, unsafe_allow_html=True)

    # --- Use markdown for the header as requested ---
    st.markdown("<h1 style='text-align: center; color: #1A2B4D;'>Admin Login</h1>", unsafe_allow_html=True)

    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="admin-login-button">', unsafe_allow_html=True)

        # --- (1) MODIFIED LOGIN LOGIC ---
        if st.button("Login", use_container_width=True):

            # --- (2) NEW VALIDATION BLOCK ---
            if not username.strip():
                st.error("Username is required.")
            elif not password:
                st.error("Password is required.")
            # --- END VALIDATION ---

            else:
                # (3) Only check credentials if both fields are filled
                if username == "admin" and password == "1234":
                    with st.spinner("Authenticating..."):
                        time.sleep(1)
                        st.session_state.logged_in = True
                        st.session_state.user_role = "Admin"
                        st.success(f"✅ Welcome, Admin!")
                        time.sleep(1)
                        st.switch_page("pages/dashboard.py")
                else:
                    # This now only runs if validation passed but credentials failed
                    st.error("Incorrect username or password.")
        # --- END MODIFIED LOGIC ---

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Wrap Back button in its CSS class
        st.markdown('<div class="admin-back-button">', unsafe_allow_html=True)
        if st.button("Back to Dashboard", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Additional Info (Unchanged)
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