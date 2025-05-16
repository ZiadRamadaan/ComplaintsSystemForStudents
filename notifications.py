import streamlit as st

def display_notifications():
    if "notifications" in st.session_state and st.session_state.notifications:
        for message in st.session_state.notifications:
            st.success(message)
        st.session_state.notifications.clear()
