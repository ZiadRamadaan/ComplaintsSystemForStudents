import smtplib
from email.message import EmailMessage
import sqlite3
import streamlit as st

EMAIL_SENDER = st.secrets["email"]["sender"]
EMAIL_PASSWORD = st.secrets["email"]["password"]
EMAIL_RECEIVER = "esraamaghrabi14@gmail.com"  # Admin email

# Fetch student email and name
def get_student_email(student_id):
    try:
        conn = sqlite3.connect("university.db")
        cursor = conn.cursor()
        cursor.execute("SELECT email, name FROM students WHERE student_id = ?", (student_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            return result[0], result[1]  # email, name
        return None, None
    except Exception as e:
        print(f"Database Error: {e}")
        return None, None

# Send email notifications
def send_complaint_email(student_id, category, priority, content, language="English"):
    user_email, name = get_student_email(student_id)

    if not user_email:
        st.error("Student ID not found in the database.")
        return False

    try:
        # Email to student
        msg_student = EmailMessage()
        msg_student['From'] = EMAIL_SENDER
        msg_student['To'] = user_email
        msg_student['Subject'] = "Complaint Received"
        msg_student.set_content(
            f"Dear {name},\n\n"
            "We have received your complaint and it has been submitted to our system.\n"
            "Our team is reviewing it and will take the necessary actions shortly.\n\n"
            "Thank you for contacting us.\n\n"
            "Best regards,\n"
            "Complaints Management Team"
        )

        # Email to admin
        msg_admin = EmailMessage()
        msg_admin['From'] = EMAIL_SENDER
        msg_admin['To'] = EMAIL_RECEIVER
        msg_admin['Subject'] = "New Complaint Submitted"
        msg_admin.set_content(
            f"A new complaint has been submitted:\n\n"
            f"Name: {name}\n"
            f"Student ID: {student_id}\n"
            f"Email: {user_email}\n"
            f"Category: {category}\n"
            f"Priority: {priority}\n"
            f"Complaint Content:\n{content}\n\n"
            "Please follow up on this complaint via the admin dashboard."
        )

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(msg_student)
            smtp.send_message(msg_admin)

        return True

    except smtplib.SMTPAuthenticationError as e:
        print(f"Authentication Error: {e}")
        st.error("Email authentication failed.")
        return False
    except smtplib.SMTPException as e:
        print(f"SMTP Error: {e}")
        st.error("Failed to send email. Please try again later.")
        return False
    except Exception as e:
        print(f"General Error: {e}")
        st.error("An unexpected error occurred while sending the email.")
        return False
