import streamlit as st
import sqlite3
from language import TEXTS
from database import get_db_connection, initialize_db, authenticate, change_password, create_default_admin
from complaints import file_complaint, manage_complaints
from notifications import display_notifications
from export import export_data
from analytics import show_analytics

# Page config
st.set_page_config(page_title="Complaints Management System", layout="wide")

# إضافة ستايل الأزرار
st.markdown("""
    <style>
    /* --- Buttons Styling --- */
    .stButton > button {
        background-color: #416445;
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
        background-color: #36543a;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "language" not in st.session_state:
    st.session_state.language = "English"
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "notifications" not in st.session_state:
    st.session_state.notifications = []
if "username" not in st.session_state:
    st.session_state.username = ""

# Database connection and initialization
conn = get_db_connection()
initialize_db(conn)
create_default_admin(conn, "admin", "1234")  # باسورد افتراضي

# Language selector sidebar
st.sidebar.subheader("Language")
language = st.sidebar.selectbox("Select Language", ["English", "Arabic"], index=0 if st.session_state.language == "English" else 1)
if language != st.session_state.language:
    st.session_state.language = language
    st.experimental_rerun()

texts = TEXTS[st.session_state.language]

# Show avatar and username at the top of sidebar if logged in
if st.session_state.authenticated:
    st.sidebar.image(
        "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png",
        width=80
    )
    st.sidebar.markdown(
        f"<div style='text-align: center; font-weight: bold; margin-bottom: 20px;'>{st.session_state.username}</div>",
        unsafe_allow_html=True
    )

# Admin login UI (only if not authenticated)
if not st.session_state.authenticated:
    admin_login_expanded = st.expander(texts["admin_expander"], expanded=False)
    with admin_login_expanded:
        st.subheader(texts["admin_login"])
        username = st.text_input(texts["username"], key="login_username")
        password = st.text_input(texts["password"], type="password", key="login_password")

        if st.button(texts["login_button"], key="login_button"):
            success, first_login = authenticate(username, password, conn)
            if success:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.first_login = first_login
                st.success(texts["login_success"])
                st.experimental_rerun()
            else:
                st.error(texts["login_error"])

# Sidebar options for sections based on authentication
sections = [texts["manage_complaints"], texts["analytics"], texts["export_data"]] if st.session_state.authenticated else [texts["file_complaint"]]
section = st.sidebar.selectbox(texts["select_section"], sections)

# Password change required on first login
if st.session_state.authenticated:
    if "first_login" in st.session_state and st.session_state.first_login:
        st.warning("You are using the default password. Please change it to continue.")

        st.subheader("Change Your Password")
        old_password = st.text_input("Enter old password", type="password", key="old_pass_first_login")
        new_password = st.text_input("Enter new password", type="password", key="new_pass_first_login")
        confirm_password = st.text_input("Confirm new password", type="password", key="confirm_pass_first_login")

        if new_password and confirm_password and new_password == confirm_password:
            if st.button("Change Password", key="change_pass_first_login_button"):
                success = change_password(st.session_state.username, old_password, new_password, conn)
                if success:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE admins SET first_login = 0 WHERE username = ?", (st.session_state.username,))
                    conn.commit()

                    st.success("Password updated successfully!")
                    st.session_state.first_login = False
                    st.experimental_rerun()
                else:
                    st.error("Old password is incorrect.")
        elif new_password != confirm_password and confirm_password != "":
            st.error("New password and confirmation do not match.")

# Sidebar buttons for password change mode and logout
if st.session_state.authenticated:
    if st.sidebar.button("Change Password", key="sidebar_change_password_button"):
        st.session_state.change_password_mode = True

    if st.sidebar.button("Log out", key="log_out_button"):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.session_state.first_login = False
        st.success("You have been logged out.")
        st.experimental_rerun()

# If user requested to change password via sidebar button (optional implementation)
if st.session_state.authenticated and st.session_state.get("change_password_mode", False):
    st.subheader("Change Password")
    old_password = st.text_input("Old password", type="password", key="old_pass_sidebar")
    new_password = st.text_input("New password", type="password", key="new_pass_sidebar")
    confirm_password = st.text_input("Confirm new password", type="password", key="confirm_pass_sidebar")

    if new_password and confirm_password and new_password == confirm_password:
        if st.button("Update Password", key="update_pass_sidebar_button"):
            success = change_password(st.session_state.username, old_password, new_password, conn)
            if success:
                st.success("Password updated successfully!")
                st.session_state.change_password_mode = False
            else:
                st.error("Old password is incorrect.")
    elif new_password != confirm_password and confirm_password != "":
        st.error("New password and confirmation do not match.")

# Show the selected section content
if section == texts["file_complaint"] and not st.session_state.authenticated:
    file_complaint(conn, texts)

if section == texts["manage_complaints"] and st.session_state.authenticated:
    manage_complaints(conn, texts)

if section == texts["export_data"] and st.session_state.authenticated:
    export_data(conn, texts)

if section == texts["analytics"] and st.session_state.authenticated:
    show_analytics(conn, texts)

# Show notifications (independent of auth state)
display_notifications()
