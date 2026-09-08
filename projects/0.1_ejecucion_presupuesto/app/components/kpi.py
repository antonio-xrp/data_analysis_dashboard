import streamlit as st


def render_kpi(
    title: str,
    value: str,
    icon: str,
    variant: str = "blue"
):
    html = (
        f'<div class="kpi-card {variant}">'
        f'<div class="kpi-header">'
        f'<div class="kpi-icon">{icon}</div>'
        f'<div class="kpi-title">{title}</div>'
        f'</div>'
        f'<div class="kpi-value">{value}</div>'
        f'</div>'
    )

    st.markdown(html, unsafe_allow_html=True)