import streamlit as st
from pathlib import Path

from streamlit_autorefresh import st_autorefresh

from components.sidebar import render_sidebar

st.set_page_config(
    page_title="Smart Server Room Monitoring",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

from views.dashboard import render_dashboard
from views.audit_log import render_audit_log

BASE_DIR = Path(__file__).parent

with open(BASE_DIR / "assets" / "style.css", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True,
    )

# Rerun otomatis tiap 3 detik -- SYSTEM STATUS di sidebar jadi ikut
# ter-update sendiri tanpa perlu refresh manual (3 detik dipilih karena
# main.py juga nulis heartbeat tiap 3 detik, lihat status_writer.py).
st_autorefresh(interval=3000, key="status_autorefresh")

render_sidebar()

page = st.session_state.get("page", "dashboard")

if page == "dashboard":
    render_dashboard()

elif page == "audit":
    render_audit_log()