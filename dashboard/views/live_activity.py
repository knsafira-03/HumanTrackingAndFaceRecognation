import streamlit as st
from pathlib import Path

from services.database_service import DatabaseService
from components.activity import render_activity_card
from components.footer import render_footer


def render_live_activity():

    st.markdown(
        """
        <div class="dashboard-title">Live Activity</div>
        <div class="dashboard-sub">Riwayat lengkap aktivitas yang terdeteksi sistem</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='margin-bottom:20px'></div>", unsafe_allow_html=True)

    db = DatabaseService()

    col1, col2, col3 = st.columns([1, 1, 3])

    with col1:
        status_filter = st.selectbox(
            "Status",
            ["All", "AUTHORIZED", "UNAUTHORIZED"],
            key="live_activity_status_filter",
        )

    with col2:
        direction_filter = st.selectbox(
            "Direction",
            ["All", "MASUK", "KELUAR"],
            key="live_activity_direction_filter",
        )

    rows = db.get_activity_feed(
        limit=20,
        status=status_filter,
        direction=direction_filter,
    )

    # dashboard/views/live_activity.py -> naik 2 level ke root project
    BASE_DIR = Path(__file__).resolve().parents[2]

    st.caption(f"Menampilkan {len(rows)} aktivitas terbaru")

    if not rows:
        st.info("Belum ada aktivitas yang cocok dengan filter ini.")
        render_footer()
        return

    for row in rows:
        render_activity_card(row, BASE_DIR)

    render_footer()