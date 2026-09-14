import streamlit as st


def render_detail_panel(log):

    with st.container(border=True):

        st.image(
            log["snapshot"],
            use_container_width=True
        )

        st.subheader(log["name"])

        status_icon = "🟢" if log["status"] == "AUTHORIZED" else "🔴"

        st.markdown(f"**Status** : {status_icon} {log['status'].title()}")
        st.markdown(f"**Event** : {log['event']}")
        st.markdown(f"**Time** : {log['time']}")
        st.markdown(f"**Location** : {log['location']}")
        st.markdown(f"**Track ID** : {log['track_id']}")
        st.markdown(f"**Confidence** : {log['confidence']}")
