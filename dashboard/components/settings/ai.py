import streamlit as st


def render_ai_settings():

    with st.container(border=True):

        st.subheader("🤖 Face Recognition")

        confidence = st.slider(
            "Confidence Threshold",
            min_value=0.10,
            max_value=1.00,
            value=0.55,
            step=0.01,
        )

        st.caption(
            f"Minimum confidence for human detection ({confidence:.0%})"
        )

        st.write("")

        recognition = st.slider(
            "Recognition Distance",
            min_value=0.20,
            max_value=1.20,
            value=0.70,
            step=0.01,
        )

        st.caption(
            f"Lower value = stricter face matching ({recognition:.2f})"
        )

        st.write("")

        st.checkbox(
            "Save Snapshot",
            value=True,
        )

        st.checkbox(
            "Register Unknown Faces",
            value=True,
        )