import streamlit as st

from components.settings.camera import render_camera_settings
from components.settings.ai import render_ai_settings
from components.settings.notification import render_notification_settings
from components.settings.database import render_database_settings
from components.settings.system import render_system_information
from components.settings.actions import render_system_actions


def render_settings():

    st.markdown("## ⚙️ Settings")
    st.caption("Configure system preferences and parameters")

    st.write("")

    row1_col1, row1_col2, row1_col3 = st.columns(3)

    with row1_col1:
        render_camera_settings()

    with row1_col2:
        render_ai_settings()

    with row1_col3:
        render_notification_settings()

    st.write("")

    row2_col1, row2_col2, row2_col3 = st.columns(3)

    with row2_col1:
        render_database_settings()

    with row2_col2:
        render_system_information()

    with row2_col3:
        render_system_actions()