import json
import time
import streamlit as st
from pathlib import Path

from services.database_service import DatabaseService


STATUS_FILE = Path(__file__).resolve().parents[2] / "system_status.json"
STALE_SECONDS = 10  # kalau heartbeat lebih tua dari ini, dianggap main.py mati


def _read_heartbeat():
    if not STATUS_FILE.exists():
        return None
    try:
        with open(STATUS_FILE, "r") as f:
            data = json.load(f)
        data["is_alive"] = (time.time() - data.get("timestamp", 0)) < STALE_SECONDS
        return data
    except Exception:
        return None


def _check_database():
    try:
        conn = DatabaseService().connect()
        conn.close()
        return True
    except Exception:
        return False


def _status_item(label, state_word, online):
    dot = "🟢" if online else "🔴"
    css_class = "online" if online else "offline"
    st.markdown(
        f'<div class="status-item {css_class}">{dot} {label} {state_word}</div>',
        unsafe_allow_html=True,
    )


def render_sidebar():

    BASE_DIR = Path(__file__).resolve().parents[1]
    logo = BASE_DIR / "assets" / "logo_diskominfo.png"

    with st.sidebar:

        st.image(str(logo), use_container_width=True)

        st.markdown(
            """
            <div class="sidebar-title">
                <h2>DISKOMINFO</h2>
                <p>Kota Probolinggo</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        st.markdown(
            "<div class='sidebar-section'>MENU</div>",
            unsafe_allow_html=True,
        )

        if "page" not in st.session_state:
            st.session_state.page = "dashboard"

        if st.button("Dashboard", use_container_width=True):
            st.session_state.page = "dashboard"

        if st.button("Live Activity", use_container_width=True):
            st.session_state.page = "dashboard"

        if st.button("Audit Log", use_container_width=True):
            st.session_state.page = "audit"

        st.markdown("---")

        st.markdown(
            "<div class='sidebar-section'>SYSTEM STATUS</div>",
            unsafe_allow_html=True,
        )

        heartbeat = _read_heartbeat()
        main_alive = bool(heartbeat and heartbeat.get("is_alive"))

        yolo_online = main_alive and bool(heartbeat.get("yolo_engine"))
        face_online = main_alive and bool(heartbeat.get("face_recognition"))
        wa_online = main_alive and bool(heartbeat.get("whatsapp"))
        db_online = _check_database()

        _status_item("YOLO Engine", "Online" if yolo_online else "Offline", yolo_online)
        _status_item("Face Recognition", "Active" if face_online else "Inactive", face_online)
        _status_item("Database", "Connected" if db_online else "Disconnected", db_online)
        _status_item("WhatsApp", "Connected" if wa_online else "Failed", wa_online)

        if not main_alive:
            st.caption("⚠️ main.py tidak terdeteksi berjalan")