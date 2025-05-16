import streamlit as st
from datetime import datetime
from database import validate_student_id_only, load_data

def file_complaint(conn, texts):
    st.title(texts["new_complaint"])

    student_id = st.text_input(texts["student_id"])  # يعتمد على اللغة: "الرقم القومي" أو "Student ID"
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
                    INSERT INTO complaints (student_id, description, type, status, timestamp)
                    VALUES (?, ?, ?, 'pending', CURRENT_TIMESTAMP)
                """, (student_id, content, category))
                conn.commit()
                st.session_state.notifications.append(texts["complaint_success"])
            else:
                st.error(texts["student_not_found"] if "student_not_found" in texts else "Student ID not found.")

def manage_complaints(conn, texts):
    st.title(texts["manage_complaints_title"])
    complaints = load_data(conn)

    if complaints:
        for complaint in complaints:
            st.write(f"{texts['complaint_id']}: {complaint[0]} | {texts['student_id']}: {complaint[1]} | {texts['status']}: {complaint[3]}")

        complaint_id = st.text_input(texts["search_complaint"], "")
        if complaint_id:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.complaint_id, c.student_id, c.description, c.status, c.type, c.timestamp,
                       s.name, s.email, s.level, s.department
                FROM complaints c
                LEFT JOIN students s ON c.student_id = s.student_id
                WHERE c.complaint_id = ?
            """, (complaint_id,))
            complaint = cursor.fetchone()

            if complaint:
                st.subheader(texts["complaint_details"])
                st.write(f"{texts['complaint_id']}: {complaint[0]}")
                st.write(f"{texts['student_id']}: {complaint[1]}")
                st.write(f"{texts['complaint_type']}: {complaint[4]}")
                st.write(f"{texts['status']}: {complaint[3]}")
                st.write(f"{texts['complaint_content']}:\n{complaint[2]}")
                st.write(f"Timestamp: {complaint[5]}")
                st.write("---")
                st.write(texts["student_info"] if "student_info" in texts else "Student Information:")
                st.write(f"Name: {complaint[6]}")
                st.write(f"Email: {complaint[7]}")
                st.write(f"Level: {complaint[8]}")
                st.write(f"Department: {complaint[9]}")

                status = st.selectbox(
                    texts["new_status"],
                    texts["statuses"],
                    index=texts["statuses"].index(complaint[3]) if complaint[3] in texts["statuses"] else 0
                )
                if st.button(texts["update_button"]):
                    cursor.execute("UPDATE complaints SET status = ? WHERE complaint_id = ?", (status, complaint[0]))
                    conn.commit()
                    st.success(texts["status_updated"])
            else:
                st.error(texts["no_complaint"])
    else:
        st.write(texts["no_complaints"])
