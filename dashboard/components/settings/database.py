import streamlit as st


def render_database_settings():

    with st.container(border=True):

        st.subheader("🗄 Database")

        st.text_input(
            "Database File",
            value="database.db",
            disabled=True,
        )

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Database Size", "17 MB")

        with col2:
            st.metric("Total Records", "845")

        st.write("")

        left, right = st.columns(2)

        with left:
            st.button(
                "Backup Database",
                use_container_width=True,
            )

        with right:
            st.button(
                "Export Data",
                use_container_width=True,
            )