import streamlit as st
import time

def display_notifications():
    if "notifications" in st.session_state and len(st.session_state.notifications) > 0:
        for notification in st.session_state.notifications:
            st.success(notification) 
            time.sleep(2)
            st.session_state.notifications.remove(notification)
