import streamlit as st
import sqlite3
from language import TEXTS
from database import get\_db\_connection, initialize\_db, authenticate, change\_password
from complaints import file\_complaint, manage\_complaints
from notifications import display\_notifications
from export import export\_data
from analytics import show\_analytics

# ...

# Page config

st.set\_page\_config(page\_title="Complaints Management System", layout="wide")

# إضافة ستايل الأزرار من الكود الأولاني

st.markdown(""" <style>
/\* --- Buttons Styling --- \*/
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
.stButton > button\:hover {
background-color: #36543a;
} </style>
""", unsafe\_allow\_html=True)

# Initialize session state

if "language" not in st.session\_state:
st.session\_state.language = "English"
if "authenticated" not in st.session\_state:
st.session\_state.authenticated = False
if "notifications" not in st.session\_state:
st.session\_state.notifications = \[]
if "username" not in st.session\_state:
st.session\_state.username = ""

# Show avatar and username at the top of sidebar if logged in

if st.session\_state.authenticated:
st.sidebar.image(
"[https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460\_1280.png](https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png)",  # Black and white avatar icon
width=80
)
st.sidebar.markdown(
f"<div style='text-align: center; font-weight: bold; margin-bottom: 20px;'>{st.session\_state.username}</div>",
unsafe\_allow\_html=True
)

# Language selector

st.sidebar.subheader("Language")
language = st.sidebar.selectbox("Select Language", \["English", "Arabic"], index=0 if st.session\_state.language == "English" else 1)
if language != st.session\_state.language:
st.session\_state.language = language
\# st.rerun()
st.experimental\_rerun()

# Get language texts

texts = TEXTS\[st.session\_state.language]
from database import create\_default\_admin

# Database connection

conn = get\_db\_connection()
initialize\_db(conn)
create\_default\_admin(conn, "admin", "1234")  # باسورد افتراضي

# Admin login UI

if not st.session\_state.authenticated:
admin\_login\_expanded = st.expander(texts\["admin\_expander"], expanded=False)
with admin\_login\_expanded:
st.subheader(texts\["admin\_login"])
username = st.text\_input(texts\["username"])
password = st.text\_input(texts\["password"], type="password")

```
    if st.button(texts["login_button"]):
        success, first_login = authenticate(username, password, conn)
        if success:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.first_login = first_login  # تخزين قيمة first_login
            st.success(texts["login_success"])
            # st.rerun()
            st.experimental_rerun()
        else:
            st.error(texts["login_error"])
```

# Sidebar options for sections

sections = \[texts\["manage\_complaints"], texts\["analytics"], texts\["export\_data"]] if st.session\_state.authenticated else \[texts\["file\_complaint"]]
section = st.sidebar.selectbox(texts\["select\_section"], sections)

# Show buttons only for authenticated admins

if st.session\_state.authenticated:
if "first\_login" in st.session\_state and st.session\_state.first\_login:
st.warning("You are using the default password. Please change it to continue.")

```
    st.subheader("Change Your Password")
    old_password = st.text_input("Enter old password", type="password")
    new_password = st.text_input("Enter new password", type="password")
    confirm_password = st.text_input("Confirm new password", type="password")
    
    if new_password == confirm_password:
        if st.button("Change Password"):
            success = change_password(st.session_state.username, old_password, new_password, conn)
            if success:
                cursor = conn.cursor()
                cursor.execute("UPDATE admins SET first_login = 0 WHERE username = ?", (st.session_state.username,))
                conn.commit()
    
                st.success("Password updated successfully!")
                st.session_state.first_login = False
                # st.rerun()
                st.experimental_rerun()
            else:
                st.error("Old password is incorrect.")
                
```

if st.session\_state.authenticated:
if st.sidebar.button("Change Password", key="sidebar\_change\_password\_button"):
st.session\_state.change\_password\_mode = True

if st.session\_state.authenticated:
if st.sidebar.button("Log out", key="log\_out\_button"):
st.session\_state.authenticated = False
st.session\_state.username = ""
st.session\_state.first\_login = False
st.success("You have been logged out.")
st.experimental\_rerun()

# File complaint (for normal users)

if section == texts\["file\_complaint"] and not st.session\_state.authenticated:
file\_complaint(conn, texts)

# Manage complaints (admin only)

if section == texts\["manage\_complaints"] and st.session\_state.authenticated:
manage\_complaints(conn, texts)

# Export data

if section == texts\["export\_data"] and st.session\_state.authenticated:
export\_data(conn, texts)

# Analytics

if section == texts\["analytics"] and st.session\_state.authenticated:
show\_analytics(conn, texts)

# Notifications

display\_notifications() # زر تسجيل الدخول
