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


def render_activity():

    db = DatabaseService()
    rows = db.get_recent_activity(10)

    BASE_DIR = Path(__file__).resolve().parents[2]

    # ==========================
    # HEADER
    # ==========================


    st.markdown("## 📸 Live Activity")

    st.write("")

    # ==========================
    # EMPTY
    # ==========================

    if len(rows) == 0:
        st.info("Belum ada aktivitas.")
        return

    # ==========================
    # CARD
    # ==========================

    for row in rows:

        timestamp, track_id, name, status, direction, snapshot = row

        image_path = None

        if snapshot:
            image = BASE_DIR / snapshot
            if image.exists():
                image_path = str(image)

        badge_class = "badge-success"
        badge_text = "🟢 AUTHORIZED"
        description = "Registered User"

        if status != "AUTHORIZED":
            badge_class = "badge-danger"
            badge_text = "🔴 UNAUTHORIZED"
            description = "Unknown Person"

        if direction.upper() == "IN":
            direction_text = "📍 Entrance"
        else:
            direction_text = "📍 Exit"

        cols = st.columns([1, 4.5], gap="small")

        with cols[0]:

            if image_path:
                st.image(
                    image_path,
                    width=170,
                )
            else:
                st.image(
                    "https://placehold.co/300x300",
                    width=170,
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

<div>
{direction_text}
</div>

<div>
🕒 {format_time(timestamp)}
</div>

<div>
🆔 Track #{track_id}
</div>

</div>

</div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<div style='margin-bottom:18px'></div>", unsafe_allow_html=True)