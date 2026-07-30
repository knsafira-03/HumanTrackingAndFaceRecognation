import streamlit as st


def render_audit_header():

    left, right = st.columns([6, 1])

    with left:

        st.markdown("## 📋 Audit Log")
        st.caption("All system access and detection events")

    with right:

        st.write("")
        st.write("")

        st.button(
            "⬇ Export CSV",
            use_container_width=True,
            key="export_csv"
        )