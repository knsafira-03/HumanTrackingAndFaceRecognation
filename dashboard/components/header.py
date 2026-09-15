import streamlit as st

from services.system_status_service import is_system_alive


def render_header():

    col1, col2 = st.columns([8, 2])

    with col1:

        st.title("Smart Server Room Access Monitoring")

        st.write("Dinas Komunikasi dan Informatika Kota Probolinggo")

        st.caption("Kota Probolinggo")

    with col2:

        st.write("")  # dorong sedikit ke bawah biar sejajar dengan judul

        online = is_system_alive()

        badge_class = "system-status-online" if online else "system-status-offline"
        label = "SYSTEM ONLINE" if online else "SYSTEM OFFLINE"

        st.markdown(
            f'<div class="system-status-badge {badge_class}">'
            f'<span class="system-status-dot"></span>{label}'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.divider()