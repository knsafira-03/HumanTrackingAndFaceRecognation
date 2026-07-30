import streamlit as st


def render_system_actions():

    with st.container(border=True):

        st.subheader("⚙️ System Actions")

        st.button(
            "Restart Service",
            use_container_width=True,
            type="primary",
        )

        st.button(
            "Clear Cache 🧹",
            use_container_width=True,
        )

        st.button(
            "Reset Settings 🚨",
            use_container_width=True,
        )