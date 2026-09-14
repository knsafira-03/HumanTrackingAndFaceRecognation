import streamlit as st

from components.audit.header import render_audit_header
from components.audit.filters import render_audit_filters
from components.audit.table import get_filtered_logs, render_audit_table
from components.audit.detail import render_detail_panel


def render_audit_log():

    # Catatan soal urutan: get_filtered_logs() dipanggil SEBELUM widget
    # filter di bawah dirender. Ini aman di Streamlit -- begitu user
    # mengubah sebuah widget, session_state-nya sudah ter-update duluan
    # SEBELUM script dijalankan ulang dari atas. Jadi filter yang paling
    # baru tetap kebaca meski urutan render di layar (header di atas,
    # filter di bawah) dibalik dari urutan baca datanya.
    logs = get_filtered_logs()

    render_audit_header(logs)

    st.write("")

    render_audit_filters()

    st.write("")

    left, right = st.columns(
        [4, 1.3],
        gap="large"
    )

    with left:

        selected_log = render_audit_table(logs)

    with right:

        if selected_log is not None:
            render_detail_panel(selected_log)
        else:
            st.info("Tidak ada data untuk ditampilkan.")
