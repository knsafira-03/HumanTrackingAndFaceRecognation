import streamlit as st
from services.database_service import DatabaseService
from services.system_status_service import read_heartbeat

def render_metrics():
    db = DatabaseService()
    metrics = db.get_metrics()
    unauthorized = db.get_unauthorized_count()

    # Current Occupancy = jumlah orang yang KAMERA lihat SAAT INI
    # (live, dari main.py), BUKAN hitungan historis MASUK-KELUAR hari
    # ini. Kalau main.py tidak terdeteksi jalan (heartbeat basi/mati,
    # misal kamera baru dimatikan), otomatis 0 -- karena memang tidak
    # ada yang sedang dipantau.
    heartbeat = read_heartbeat()

    if heartbeat and heartbeat.get("is_alive"):
        occupancy = heartbeat.get("person_count", 0)
    else:
        occupancy = 0

    c1, c2, c3, c4 = st.columns(4)

    cards = [

    (
    c1,
    "👥",
    "Current Occupancy",
    occupancy,
    "People Inside",
    "#0EA5E9"
    ),

    (
    c2,
    "📥",
    "Today's Entry",
    metrics["entrance"],
    "Today",
    "#0284C7"
    ),

    (
    c3,
    "📤",
    "Today's Exit",
    metrics["exit"],
    "Today",
    "#4F46E5"
    ),

    (
    c4,
    "🚨",
    "Unauthorized",
    unauthorized,
    "Alert",
    "#DC2626"
    )
    ]

    for col, icon, title, value, subtitle, color in cards:

        with col:
            st.markdown(
    f"""
<div class="metric-card">

<div class="metric-circle" style="background:{color};">
{icon}
</div>

<div class="metric-header">
{title}
</div>

<div class="metric-number">
{value}
</div>

<div class="metric-footer">
{subtitle}
</div>

</div>
""",
    unsafe_allow_html=True
)