import pandas as pd
import streamlit as st

def export_data(conn, texts):
    st.title(texts["export_title"])

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM complaints")
    complaints_data = cursor.fetchall()

    if complaints_data:
        df = pd.DataFrame(complaints_data, columns=[
            "complaint_id",
            "student_id",
            "description",
            "status",
            "type",
            "timestamp"
        ])

        csv = df.to_csv(index=False)
        st.download_button(
            label=texts["download_csv"],
            data=csv,
            file_name="complaints_data.csv",
            mime="text/csv"
        )
    else:
        st.write(texts["no_data_export"])

