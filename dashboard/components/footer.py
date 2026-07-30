import streamlit as st


def render_footer():

    st.divider()

    st.markdown(
        """
<div class="footer">

<h3>
Smart Server Room Access Monitoring
</h3>

<p>
Dinas Komunikasi dan Informatika Kota Probolinggo
</p>

<p class="footer-tech">
Powered by YOLOv8 • FaceNet • Streamlit
</p>

<p class="footer-copy">
© 2026 Universitas Brawijaya
</p>

</div>
""",
        unsafe_allow_html=True
    )