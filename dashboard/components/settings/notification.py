import streamlit as st


def render_notification_settings():

    with st.container(border=True):

        st.subheader("📱 Notification Settings")

        st.checkbox(
            "WhatsApp Notification",
            value=True,
        )

        st.checkbox(
            "Save Image to Database",
            value=True,
        )

        st.text_input(
            "Phone Number",
            placeholder="+628xxxxxxxxxx",
        )

        st.write("")

        st.button(
            "Test Notification 🚀",
            use_container_width=True,
        )