import streamlit as st


def render_header():

    col1, col2 = st.columns([8,2])

    with col1:

        st.title("Smart Server Room Access Monitoring")

        st.write("Dinas Komunikasi dan Informatika Kota Probolinggo")

        st.caption("Kota Probolinggo")

    with col2:

        st.success("🟢 SYSTEM ONLINE")

    st.divider()