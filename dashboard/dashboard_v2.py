import streamlit as st
from pathlib import Path

from components.sidebar import render_sidebar

st.set_page_config(
    page_title="Smart Server Room Monitoring",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

from views.dashboard import render_dashboard
from views.audit_log import render_audit_log
from views.live_activity import render_live_activity

BASE_DIR = Path(__file__).parent

with open(BASE_DIR / "assets" / "style.css", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True,
    )

render_sidebar()

page = st.session_state.get("page", "dashboard")

if page == "dashboard":
    render_dashboard()

elif page == "audit":
    render_audit_log()

elif page == "live_activity":
    render_live_activity()