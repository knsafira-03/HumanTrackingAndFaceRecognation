import streamlit as st
from pathlib import Path


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

        if st.button("🏠 Dashboard", use_container_width=True):
            st.session_state.page = "dashboard"

        if st.button("📸 Live Activity", use_container_width=True):
            st.session_state.page = "dashboard"

        if st.button("📊 Analytics", use_container_width=True):
            st.session_state.page = "analytics"

        if st.button("📋 Audit Log", use_container_width=True):
            st.session_state.page = "audit"

        if st.button("⚙ Settings", use_container_width=True):
            st.session_state.page = "settings"

        st.markdown("---")

        st.markdown(
            "<div class='sidebar-section'>SYSTEM STATUS</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="status-item online">🟢 YOLO Engine Online</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="status-item online">🟢 Face Recognition Active</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="status-item online">🟢 Database Connected</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="status-item online">🟢 WhatsApp Connected</div>',
            unsafe_allow_html=True,
        )