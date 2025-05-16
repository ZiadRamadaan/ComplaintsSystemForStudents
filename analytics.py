import streamlit as st
import plotly.express as px
import plotly.io as pio
import pandas as pd

pio.templates.default = "plotly_white"

colors = ["#03265b", "#416445", "#38b6ff"]

def show_analytics(conn, texts):
    st.markdown("<h2 style='color:#2c3e50;'>Analytics</h2>", unsafe_allow_html=True)

    cursor = conn.cursor()
    cursor.execute("SELECT complaint_id, student_id, description, status, type, timestamp FROM complaints")
    complaints_data = cursor.fetchall()

    if complaints_data:
        df = pd.DataFrame(complaints_data, columns=[
            "complaint_id", "student_id", "description", "status", "type", "timestamp"
        ])
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')

        # KPIs
        total = len(df)
        resolved_statuses = ["closed"]  # الحالة المعتمدة كمحلولة
        resolved = len(df[df["status"].str.lower().isin(resolved_statuses)])
        unresolved = total - resolved
        percent_resolved = (resolved / total) * 100 if total > 0 else 0

        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric(label="Total Complaints", value=total)
        kpi2.metric(label="Closed Complaints", value=resolved)
        kpi3.metric(label="Closure Rate", value=f"{percent_resolved:.2f}%")

        st.markdown("---")

        # Charts Row 1: Complaint Type & Status Pie Charts
        row1_col1, row1_col2 = st.columns(2)

        with row1_col1:
            fig_type = px.pie(df, names="type", title="Complaints by Type", color_discrete_sequence=colors)
            fig_type.update_traces(textinfo="percent+label", pull=0.03)
            fig_type.update_layout(title_font_size=18, title_font_color="#2c3e50")
            st.plotly_chart(fig_type, use_container_width=True)

        with row1_col2:
            fig_status = px.pie(df, names="status", title="Complaints by Status", color_discrete_sequence=colors)
            fig_status.update_traces(textinfo="percent+label", pull=0.03)
            fig_status.update_layout(title_font_size=18, title_font_color="#2c3e50")
            st.plotly_chart(fig_status, use_container_width=True)

        # Charts Row 2: Complaints Over Time Line Chart
        row2_col1, _ = st.columns(2)

        with row2_col1:
            df_monthly = df.groupby(df["timestamp"].dt.to_period("M")).size().reset_index(name="count")
            df_monthly["timestamp"] = df_monthly["timestamp"].astype(str)
            fig_time = px.line(df_monthly, x="timestamp", y="count", markers=True, title="Monthly Complaint Trend")
            fig_time.update_traces(line_shape="linear", marker=dict(color=colors[0]))
            fig_time.update_layout(
                title_font_size=18,
                xaxis_title="Month",
                yaxis_title="Number of Complaints",
                title_font_color="#2c3e50"
            )
            st.plotly_chart(fig_time, use_container_width=True)

    else:
        st.warning("No complaint data found in the database.")
