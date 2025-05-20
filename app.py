import streamlit as st
import sqlite3
from language import TEXTS
from database import get_db_connection, initialize_db, authenticate, change_password, create_default_admin
from complaints import file_complaint, manage_complaints
from notifications import display_notifications
from export import export_data
from analytics import show_analytics
from email_utils import send_complaint_email

# Page config
st.set_page_config(page_title="Complaints Management System", layout="wide")

# Button Styling
st.markdown("""
    <style>
    .stButton > button {
        background-color: #5599ff;
        color: #FFFFFF !important;
        border: none;
        border-radius: 5px;
        padding: 8px 15px !important; 
        font-size: 14px !important;
        font-weight: bold;
        transition: background-color 0.3s;
        text-align: center;
    }
    .stButton > button:hover {
        background-color: #4177cc;
    }
    .custom-navbar {
        background-color: #FFFFFF;
        padding: 10px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        direction: rtl;
    }

    .custom-navbar img {
        height: 60px;
    }

    .logo-right, .logo-left {
        display: flex;
        align-items: center;
    }
    </style>

    <div class="custom-navbar">
        <div class="logo-right">
            <img src="https://ci.tanta.edu.eg/images/logo.png" alt="Right Logo">
        </div>
        <div class="logo-right">
            <img src="https://tdb.tanta.edu.eg/ebooks/assets/img/tanta-logo.png" alt="Right Logo">
        </div>
    </div>
    </style>
""", unsafe_allow_html=True)

# Session state initialization
if "language" not in st.session_state:
    st.session_state.language = "English"
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "notifications" not in st.session_state:
    st.session_state.notifications = []
if "username" not in st.session_state:
    st.session_state.username = ""
if "change_password_mode" not in st.session_state:
    st.session_state.change_password_mode = False

# Sidebar avatar
if st.session_state.authenticated:
    st.sidebar.markdown(
        """
        <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
            <img src="https://cdn.pixabay.com/photo/2018/04/18/18/56/user-3331257_640.png" width="80">
        </div>
        """,
        unsafe_allow_html=True
    )
    st.sidebar.markdown(
        f"<div style='text-align: center; font-weight: bold; margin-bottom: 20px;'>{st.session_state.username}</div>",
        unsafe_allow_html=True
    )

# Language selector
st.sidebar.subheader("Language")
language = st.sidebar.selectbox("Select Language", ["English", "Arabic"], index=0 if st.session_state.language == "English" else 1)
if language != st.session_state.language:
    st.session_state.language = language
    st.rerun()

# Get translated texts
texts = TEXTS[st.session_state.language]

# Database connection and initialization
conn = get_db_connection()
initialize_db(conn)
create_default_admin(conn, "admin", "1234")  # This function should already check if admin exists

# Admin login UI
if not st.session_state.authenticated:
    admin_login_expanded = st.expander(texts["admin_expander"], expanded=False)
    with admin_login_expanded:
        st.subheader(texts["admin_login"])
        username = st.text_input(texts["username"])
        password = st.text_input(texts["password"], type="password")

        if st.button(texts["login_button"]):
            success, first_login = authenticate(username, password, conn)
            if success:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.first_login = first_login
                st.success(texts["login_success"])
                st.rerun()
            else:
                st.error(texts["login_error"])

# Sections based on login status
sections = [texts["manage_complaints"], texts["analytics"], texts["export_data"]] if st.session_state.authenticated else [texts["file_complaint"]]
section = st.sidebar.selectbox(texts["select_section"], sections)

# Handle first login password change
if st.session_state.authenticated and st.session_state.get("first_login", False):
    st.warning(texts["first_login_warning"])

    st.subheader(texts["change_password_title"])
    old_password = st.text_input(texts["old_password"], type="password")
    new_password = st.text_input(texts["new_password"], type="password")
    confirm_password = st.text_input(texts["confirm_password"], type="password")

    if new_password != confirm_password:
        st.error(texts["password_mismatch"])
    elif st.button(texts["change_password_button"], key="change_password_button_first"):
        success = change_password(st.session_state.username, old_password, new_password, conn)
        if success:
            cursor = conn.cursor()
            cursor.execute("UPDATE admins SET first_login = 0 WHERE username = ?", (st.session_state.username,))
            conn.commit()
            st.success(texts["password_changed"])
            st.session_state.first_login = False
            st.rerun()
        else:
            st.error(texts["incorrect_old_password"])

# Show sidebar change password option
if st.session_state.authenticated:
    if st.sidebar.button(texts["sidebar_change_password"], key="sidebar_change_password"):
        st.session_state.change_password_mode = True
        st.sidebar.markdown("---")

# Handle password change mode
if st.session_state.authenticated and st.session_state.change_password_mode:
    st.subheader(texts["change_password_title"])
    old_password = st.text_input(texts["old_password"], type="password")
    new_password = st.text_input(texts["new_password"], type="password")
    confirm_password = st.text_input(texts["confirm_password"], type="password")

    if new_password != confirm_password:
        st.error(texts["password_mismatch"])
    elif st.button(texts["change_password_button"], key="change_password_button_sidebar"):
        success = change_password(st.session_state.username, old_password, new_password, conn)
        if success:
            st.success(texts["password_changed"])
            st.session_state.change_password_mode = False
            st.rerun()
        else:
            st.error(texts["incorrect_old_password"])

# Log out button
if st.session_state.authenticated:
    if st.sidebar.button(texts["logout"]):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.session_state.first_login = False
        st.success(texts["log_out_success"])
        st.rerun()

# Sections routing
if section == texts["file_complaint"] and not st.session_state.authenticated:
    file_complaint(conn, texts)

if section == texts["manage_complaints"] and st.session_state.authenticated:
    manage_complaints(conn, texts)

if section == texts["export_data"] and st.session_state.authenticated:
    export_data(conn, texts)

if section == texts["analytics"] and st.session_state.authenticated:
    show_analytics(conn, texts)

# Notifications
display_notifications()
