import streamlit as st

from components.audit.header import render_audit_header
from components.audit.filters import render_audit_filters
from components.audit.table import render_audit_table
from components.audit.detail import render_detail_panel


def render_audit_log():

    render_audit_header()

    st.write("")

    render_audit_filters()

    st.write("")

    left, right = st.columns(
        [4, 1.3],
        gap="large"
    )

    with left:

        render_audit_table()

        dummy_log = {
        "name": "Khalisa",
        "role": "Registered User",
        "status": "AUTHORIZED",
        "event": "Entry",
        "time": "30 Jul 2026 09:48:12",
        "location": "Server Room",
        "track_id": "#13",
        "confidence": 99.41,
        "snapshot": "https://placehold.co/300x300",
    }

    with right:

        render_detail_panel(dummy_log)