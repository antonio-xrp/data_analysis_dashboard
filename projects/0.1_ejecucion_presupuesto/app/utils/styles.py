import streamlit as st
from pathlib import Path


def load_css(file_path):
    with open(file_path) as f:
        st.markdown(
            f"""
            <style>
                {f.read()}
            </style>
            """,
            unsafe_allow_html=True
        )