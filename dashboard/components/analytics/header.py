import streamlit as st


def render_header():

    left, right = st.columns([4,2])

    with left:

        st.markdown("""
        <h1 style="
            margin-bottom:0;
            font-size:34px;
        ">
        📊 Analytics
        </h1>
        """, unsafe_allow_html=True)

        st.caption(
            "System statistics and activity insights"
        )

    with right:

        c1, c2 = st.columns([3,2])

        with c1:

            st.date_input(
                " ",
                value=None,
                label_visibility="collapsed",
                width="stretch"
            )

        with c2:

            st.button(
                "📥 Export Report",
                width="stretch"
            )

    st.write("")