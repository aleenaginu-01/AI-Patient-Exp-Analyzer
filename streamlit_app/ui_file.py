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

    .stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
    }

    /* Hide Streamlit branding and sidebar */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}
    section[data-testid="stSidebar"] {display: none;}
    .css-1d391kg {display: none;}

    /* Main container */
    .main-container {
        background: #fffbeb;
        border-radius: 20px;
        padding: 40px;
        margin: 20px auto;
        max-width: 1200px;
        box-shadow: 0 20px 60px rgba(20, 184, 166, 0.3);
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
        background: linear-gradient(135deg, #14b8a6 0%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }

    .tagline {
        color: #0f766e;
        font-size: 18px;
        font-weight: 400;
    }

    /* Stats Cards */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
        margin: 30px 0;
    }

    .stat-card {
        background: linear-gradient(135deg, #14b8a6 0%, #06b6d4 100%);
        border-radius: 15px;
        padding: 25px;
        color: white;
        box-shadow: 0 10px 30px rgba(20, 184, 166, 0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        animation: slideIn 0.6s ease-out;
    }

    .stat-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 40px rgba(20, 184, 166, 0.5);
    }

    .stat-number {
        font-size: 36px;
        font-weight: 700;
        margin: 10px 0;
    }

    .stat-label {
        font-size: 14px;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Login Button */
    .login-btn-container {
        text-align: center;
        margin: 40px 0;
    }

    /* Features Section */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 25px;
        margin-top: 40px;
    }

    .feature-card {
        background: linear-gradient(135deg, #14b8a6 0%, #06b6d4 100%);
        border-radius: 15px;
        padding: 30px;
        border: 2px solid #a7f3d0;
        transition: all 0.3s ease;
        animation: fadeInUp 0.8s ease-out;
    }

    .feature-card:hover {
        border-color: #14b8a6;
        box-shadow: 0 10px 30px rgba(20, 184, 166, 0.2);
        transform: translateY(-5px);
    }

    .feature-icon {
        font-size: 40px;
        margin-bottom: 15px;
    }

    .feature-title {
        font-size: 20px;
        font-weight: 600;
        color: #0f766e;
        margin-bottom: 10px;
    }

    .feature-desc {
        color: #115e59;
        font-size: 14px;
        line-height: 1.6;
    }

    /* Login Form Styles */
    .login-container {
        max-width: 450px;
        margin: 50px auto;
        background: #fffbeb;
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 20px 60px rgba(20, 184, 166, 0.3);
        animation: fadeInUp 0.6s ease-out;
    }

    .login-header {
        text-align: center;
        margin-bottom: 30px;
    }

    .login-title {
        font-size: 32px;
        font-weight: 700;
        background: linear-gradient(135deg, #14b8a6 0%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }

    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #14b8a6 0%, #06b6d4 100%);
        color: black;
        border: none;
        padding: 15px 30px;
        font-size: 16px;
        font-weight: 600;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(20, 184, 166, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(20, 184, 166, 0.4);
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

    /* Pulse Animation */
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
    }

    .pulse {
        animation: pulse 2s infinite;
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
            <div class="stat-label">Active Patients</div>
            <div class="stat-number">2,847</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Today's Appointments</div>
            <div class="stat-number">156</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Available Doctors</div>
            <div class="stat-number">42</div>
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
            <p style="color: #0f766e; margin-top: 10px;">Sign in to your account</p>
        </div>
    """, unsafe_allow_html=True)

    # Role Selection
    role = st.selectbox(
        "Select Your Role",
        ["Patient", "Admin"],
        index=0
    )

    if role =="Admin":
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Login", use_container_width=True):
                if username =="admin" and password =="1234":
                    with st.spinner("Authenticating..."):
                        time.sleep(1)
                        st.session_state.logged_in = True
                        st.session_state.user_role = role
                        st.success(f"✅ Welcome, Admin!")
                        time.sleep(1)
                        st.switch_page("pages/dashboard.py")
                        # st.balloons()
                else:
                    st.error("Please enter both username and password")

        with col2:
            if st.button("Back to Dashboard", use_container_width=True):
                st.session_state.page = 'dashboard'
                st.rerun()

    elif role == "Patient":
        # st.subheader(" Patient Login")
        patient_id = st.text_input("Enter Patient ID or Phone Number")

        if st.button("Login as Patient"):
            if patient_id.strip() == "LIS123":
                st.success("Welcome! Redirecting to your User Page...")
                st.session_state["user_role"] = "patient"
                st.session_state["patient_id"] = patient_id
                st.switch_page("pages/user.py")
            else:
                st.warning("Please enter your Patient ID or Phone Number.")


    st.markdown("</div>", unsafe_allow_html=True)

    # Additional Info
    st.markdown("""
    <div style="text-align: center; margin-top: 30px; color: white;">
        <p style="font-size: 14px;">Don't have an account? <a href="#" style="color: white; font-weight: 600;">Contact Administrator</a></p>
        <p style="font-size: 12px; margin-top: 10px; opacity: 0.8;">© 2024 CareLoop.ai - All rights reserved</p>
    </div>
    """, unsafe_allow_html=True)


# Main App Logic
if st.session_state.page == 'dashboard':
    show_dashboard()
elif st.session_state.page == 'login':
    show_login()