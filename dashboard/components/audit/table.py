import streamlit as st
import pandas as pd


def render_audit_table():

    df = pd.DataFrame(
        [
            {
                "Time": "09:48:12",
                "User": "Khalisa",
                "Event": "Entry",
                "Status": "Authorized",
                "Location": "Server Room",
                "Confidence": "99.41%",
                "Track ID": "#13",
                "Snapshot": "📷",
            },
            {
                "Time": "09:51:33",
                "User": "Unknown",
                "Event": "Exit",
                "Status": "Unauthorized",
                "Location": "Server Room",
                "Confidence": "45.22%",
                "Track ID": "#14",
                "Snapshot": "📷",
            },
        ]
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )