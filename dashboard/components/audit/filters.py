import streamlit as st

from services.database_service import DatabaseService


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

        # value=None penting -- kalau tidak diisi, Streamlit defaultnya
        # otomatis TANGGAL HARI INI, yang bikin tabel keliatan kosong
        # begitu filter tanggal diterapkan (karena data lama gak match
        # "hari ini"). Dengan None, filter tanggal jadi opsional/off
        # sampai user benar-benar pilih tanggal.
        st.date_input(
            "",
            value=None,
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

        known_users = DatabaseService().get_distinct_users()

        st.selectbox(
            "",
            ["All Users"] + known_users,
            key="audit_user"
        )
