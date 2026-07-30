import streamlit as st
import pandas as pd


def render_table():

    data = pd.DataFrame(
        {
            "#": [1, 2, 3, 4, 5],
            "User": [
                "🟢 Khalisa",
                "🟢 Aqila",
                "🟢 Raras",
                "🟢 Bima",
                "🔴 Unknown",
            ],
            "Total": [31, 28, 22, 22, 18],
            "Entry": [18, 16, 10, 10, 6],
            "Exit": [13, 12, 12, 12, 12],
            "Last Seen": [
                "09:48",
                "09:43",
                "09:21",
                "09:20",
                "08:55",
            ],
        }
    )

    with st.container(border=True):

        header_left, header_right = st.columns([5, 1])

        with header_left:
            st.markdown(
                """
                <div class="analytics-section-title">
                    Top Registered Users
                </div>
                """,
                unsafe_allow_html=True,
            )

        with header_right:
            st.caption("Today")

        st.dataframe(
            data,
            use_container_width=True,
            hide_index=True,
        )