import streamlit as st


def render_camera_settings():

    with st.container(border=True):

        st.subheader("📷 Camera Settings")

        st.selectbox(
            "Camera Source",
            [
                "USB Camera (0)",
                "USB Camera (1)",
            ]
        )

        st.selectbox(
            "Resolution",
            [
                "1920 × 1080 (Full HD)",
                "1280 × 720 (HD)",
                "640 × 480",
            ]
        )

        st.selectbox(
            "FPS",
            [
                15,
                30,
                60
            ]
        )

        st.checkbox(
            "Auto Reconnect",
            value=True
        )