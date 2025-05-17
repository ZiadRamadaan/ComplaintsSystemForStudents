import streamlit as st
from datetime import datetime
from database import validate_student_id_only, load_data
from email_utils import send_complaint_email

def file_complaint(conn, texts):
    st.title(texts["new_complaint"])

    student_id = st.text_input(texts["student_id"])
    category = st.selectbox(texts["complaint_type"], texts["complaint_types"])
    priority = st.selectbox(texts["priority"], texts["priorities"])
    content = st.text_area(texts["complaint_content"])

    if st.button(texts["submit"]):
        if not student_id or not category or not content:
            st.error(texts["fill_fields"])
        else:
            if validate_student_id_only(student_id, conn):
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO complaints (student_id, description, type, priority, status, timestamp)
                    VALUES (?, ?, ?, ?, 'pending', CURRENT_TIMESTAMP)
                """, (student_id, content, category, priority))

                conn.commit()
                st.session_state.notifications.append("Complaint submitted successfully.")
                send_complaint_email(student_id, category, priority, content, st.session_state.language)
            else:
                st.error("Student ID not found.")

def manage_complaints(conn, texts):
    status_display_to_db = {
        "Pending": "pending", "Reviewed": "reviewed", "Closed": "closed",
        "قيد الانتظار": "pending", "تم المراجعة": "reviewed", "مغلقة": "closed"
    }
    status_db_to_display = {v: k for k, v in status_display_to_db.items()}

    st.title(texts["manage_complaints_title"])
    complaints = load_data(conn)

    if complaints:
        for complaint in complaints:
            status_display = status_db_to_display.get(complaint[3], complaint[3])
            st.write(f"{texts['complaint_id']}: {complaint[0]} | {texts['student_id']}: {complaint[1]} | {texts['status']}: {status_display}")

        complaint_id = st.text_input(texts["search_complaint"], "")
        if complaint_id:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.complaint_id, c.student_id, c.description, c.status, c.type, c.priority, c.timestamp,
                       s.name, s.email, s.level, s.department
                FROM complaints c
                LEFT JOIN students s ON c.student_id = s.student_id
                WHERE c.complaint_id = ?
            """, (complaint_id,))
            complaint = cursor.fetchone()

            if complaint:
                current_status_display = status_db_to_display.get(complaint[3], complaint[3])
                st.subheader(texts["complaint_details"])
                st.write(f"{texts['complaint_id']}: {complaint[0]}")
                st.write(f"{texts['student_id']}: {complaint[1]}")
                st.write(f"{texts['complaint_type']}: {complaint[4]}")
                st.write(f"{texts['status']}: {current_status_display}")
                st.write(f"{texts['complaint_content']}:\n{complaint[2]}")
                st.write(f"{texts['priority']}: {complaint[5]}")
                st.write(f"Timestamp: {complaint[6]}")
                st.write("---")
                st.write(texts.get("student_info", "Student Information:"))
                if all(complaint[6:10]):
                    st.write(f"Name: {complaint[6]}")
                    st.write(f"Email: {complaint[7]}")
                    st.write(f"Level: {complaint[8]}")
                    st.write(f"Department: {complaint[9]}")
                else:
                    st.warning("Student information is incomplete or missing.")

                selected_display_status = st.selectbox(
                    texts["new_status"],
                    texts["statuses"],
                    index=texts["statuses"].index(current_status_display) if current_status_display in texts["statuses"] else 0
                )

                selected_db_status = status_display_to_db.get(selected_display_status)

                if selected_db_status not in ["pending", "reviewed", "closed"]:
                    st.error("Invalid status selected.")
                else:
                    if st.button(texts["update_button"]):
                        cursor.execute("UPDATE complaints SET status = ? WHERE complaint_id = ?", (selected_db_status, complaint[0]))
                        conn.commit()
                        st.success(texts["status_updated"])
            else:
                st.error(texts["no_complaint"])
    else:
        st.write(texts["no_complaints"])
