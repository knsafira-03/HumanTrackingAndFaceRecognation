import streamlit as st


def render_system_information():

    with st.container(border=True):

        st.subheader("ℹ️ System Information")

        info = {
            "Application Version": "1.0.0",
            "YOLO Model": "YOLOv8n",
            "Face Recognition": "FaceNet",
            "Python Version": "3.11.9",
            "Streamlit Version": "1.60.0",
            "Last Started": "30 Jul 2026 07:45",
        }

        for key, value in info.items():

            left, right = st.columns([2, 1])

            with left:
                st.caption(key)

            with right:
                st.write(value)