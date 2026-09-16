import streamlit as st
from pathlib import Path
from datetime import datetime

from services.database_service import DatabaseService


def format_time(timestamp):
    try:
        dt = datetime.strptime(str(timestamp), "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%d %b %Y • %H:%M")
    except:
        return str(timestamp)

def render_activity_card(row, base_dir):

    timestamp, track_id, name, status, direction, snapshot = row

    image_path = None

    if snapshot:
        image = base_dir / snapshot
        if image.exists():
            image_path = str(image)

    badge_class = "badge-success"
    badge_text = "AUTHORIZED"
    description = "Registered User"

    if status != "AUTHORIZED":
        badge_class = "badge-danger"
        badge_text = "UNAUTHORIZED"
        description = "Unknown Person"

    direction_text = "📍 Entrance" if direction.upper() == "MASUK" else "📍 Exit"

    cols = st.columns([1, 4.5], gap="small")

    with cols[0]:
        st.image(
            image_path if image_path else "https://placehold.co/300x300",
            width=150,
        )

    with cols[1]:
        st.markdown(
            f"""
<div class="activity-card">

<div class="{badge_class}">
{badge_text}
</div>

<h2>{name}</h2>

<div class="activity-desc">
{description}
</div>

<div class="activity-grid">

<div>{direction_text}</div>

<div>🕒 {format_time(timestamp)}</div>

<div>🆔 Track #{track_id}</div>

</div>

</div>
""",
            unsafe_allow_html=True,
        )

    st.markdown(
        "<div style='margin-bottom:12px'></div>",
        unsafe_allow_html=True,
    )


def render_activity():

    db = DatabaseService()

    rows = db.get_recent_activity(6)

    BASE_DIR = Path(__file__).resolve().parents[2]

    header_left, header_right = st.columns([5, 1])

    with header_left:
        st.markdown("## 📸 Live Activity")

    with header_right:

        if st.button(
            "View All →",
            key="activity_view_all",
            use_container_width=True,
        ):
            st.session_state.page = "live_activity"
            st.rerun()

    st.caption(f"Showing latest {len(rows)} activities")

    if not rows:
        st.info("Belum ada aktivitas.")
        return

    for row in rows:
        render_activity_card(row, BASE_DIR)