import streamlit as st
import plotly.express as px
import plotly.io as pio
import pandas as pd

pio.templates.default = "plotly_white"

colors = ["#03265b", "#416445", "#38b6ff"]

def show_analytics(conn, texts):
    st.markdown(f"<h2 style='color:#2c3e50;'>{texts['analytics_title']}</h2>", unsafe_allow_html=True)

    cursor = conn.cursor()
    cursor.execute("SELECT complaint_id, student_id, description, type, priority, status, timestamp FROM complaints")
    complaints_data = cursor.fetchall()

    if complaints_data:
        df = pd.DataFrame(complaints_data, columns=[
            "complaint_id", "student_id", "description", "type", "priority", "status", "timestamp"
        ])
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')

        # KPIs
        total = len(df)
        resolved = len(df[df["status"].str.lower().isin(["closed", "مغلقة"])])
        unresolved = total - resolved
        percent_resolved = (resolved / total) * 100 if total > 0 else 0

        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric(label=texts["new_complaint"], value=total)
        kpi2.metric(label=texts["statuses"][2], value=resolved)
        kpi3.metric(label="Resolution Rate", value=f"{percent_resolved:.2f}%")

        st.markdown("---")

        # Charts Row 1: Type & Priority
        row1_col1, row1_col2 = st.columns(2)

        with row1_col1:
            fig_cat = px.bar(df, x="type", color="type", title=texts["by_category"], color_discrete_sequence=colors)
            fig_cat.update_layout(title_font_size=18, title_font_color="#2c3e50")
            st.plotly_chart(fig_cat, use_container_width=True)

        with row1_col2:
            fig_pri = px.pie(df, names="priority", title=texts["by_priority"], color_discrete_sequence=colors)
            fig_pri.update_traces(textinfo="percent+label", pull=0.03)
            fig_pri.update_layout(title_font_size=18, title_font_color="#2c3e50")
            st.plotly_chart(fig_pri, use_container_width=True)

        # Charts Row 2: Status & Time Trend
        row2_col1, row2_col2 = st.columns(2)

        with row2_col1:
            fig_status = px.pie(df, names="status", title=texts["by_status"], color_discrete_sequence=colors)
            fig_status.update_traces(textinfo="percent+label", pull=0.03)
            fig_status.update_layout(title_font_size=18, title_font_color="#2c3e50")
            st.plotly_chart(fig_status, use_container_width=True)

        with row2_col2:
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
        st.warning(texts["no_data"])
