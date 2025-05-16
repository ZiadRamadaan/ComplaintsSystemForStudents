import streamlit as st
import plotly.express as px
import plotly.io as pio
import pandas as pd

pio.templates.default = "plotly_white"

colors = ["#03265b", "#416445", "#38b6ff"]

def show_analytics(conn, texts):
    st.markdown("<h2 style='color:#2c3e50;'>Analytics</h2>", unsafe_allow_html=True)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM complaints")
    complaints_data = cursor.fetchall()

    if complaints_data:
        # عدل أسماء الأعمدة حسب عدد الأعمدة في complaints_data
        # مثال: إذا فيه 6 أعمدة فقط
        df = pd.DataFrame(complaints_data, columns=[
            "id", "name", "email", "category", "content", "status"
        ])

        # لو عندك عمود created_at او priority غير موجودين في الجدول، هتعامل مع الأمر بناءً على البيانات الفعلية
        
        # لو عندك عمود تاريخ أو وقت، استخدمه لتحليل الاتجاه الزمني
        # لو مش موجود، تجاهل رسم المخطط الزمني أو استبدله بمخطط آخر

        # KPIs
        total = len(df)
        resolved_statuses = ["resolved", "تم الحل", "solved", "closed"]  # ممكن تضيف الكلمات المناسبة حسب بياناتك
        resolved = len(df[df["status"].str.lower().isin(resolved_statuses)])
        unresolved = total - resolved
        percent_resolved = (resolved / total) * 100 if total > 0 else 0

        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric(label="Total Complaints", value=total)
        kpi2.metric(label="Resolved Complaints", value=resolved)
        kpi3.metric(label="Resolution Rate", value=f"{percent_resolved:.2f}%")

        st.markdown("---")

        # Charts Row 1: Category & Status
        row1_col1, row1_col2 = st.columns(2)

        with row1_col1:
            fig_cat = px.bar(df, x="category", color="category", title="Complaints by Category", color_discrete_sequence=colors)
            fig_cat.update_layout(title_font_size=18, title_font_color="#2c3e50")
            st.plotly_chart(fig_cat, use_container_width=True)

        with row1_col2:
            fig_status = px.pie(df, names="status", title="Complaints by Status", color_discrete_sequence=colors)
            fig_status.update_traces(textinfo="percent+label", pull=0.03)
            fig_status.update_layout(title_font_size=18, title_font_color="#2c3e50")
            st.plotly_chart(fig_status, use_container_width=True)

        # لو عندك عمود created_at تقدر تضيف مخطط زمني، إذا مش موجود إحذفه

    else:
        st.warning("No complaint data found in the database.")
