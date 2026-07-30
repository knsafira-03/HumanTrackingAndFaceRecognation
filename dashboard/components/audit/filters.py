import streamlit as st


def render_audit_filters():

    c1, c2, c3, c4, c5 = st.columns(
        [3.2, 1.5, 1.3, 1.3, 1.3]
    )

    with c1:

        st.text_input(
            "",
            placeholder="Search user or event...",
            key="audit_search"
        )

    with c2:

        st.date_input(
            "",
            key="audit_date"
        )

    with c3:

        st.selectbox(
            "",
            [
                "All Events",
                "Entry",
                "Exit"
            ],
            key="audit_event"
        )

    with c4:

        st.selectbox(
            "",
            [
                "All Status",
                "Authorized",
                "Unauthorized"
            ],
            key="audit_status"
        )

    with c5:

        st.selectbox(
            "",
            [
                "All Users"
            ],
            key="audit_user"
        )