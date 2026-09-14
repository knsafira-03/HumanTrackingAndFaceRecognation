import streamlit as st
from pathlib import Path

from services.database_service import DatabaseService

BASE_DIR = Path(__file__).resolve().parents[3]


def _map_log(row):
    """
    Ubah row dari tabel `attendance`
    (id, timestamp, track_id, name, status, direction, snapshot_path, confidence)
    jadi dict yang dipakai UI audit log & detail panel.
    """

    _id, timestamp, track_id, name, status, direction, snapshot_path, confidence = row

    event = "Entry" if direction == "MASUK" else "Exit"

    snapshot = "https://placehold.co/300x300"
    if snapshot_path:
        full_path = BASE_DIR / snapshot_path
        if full_path.exists():
            snapshot = str(full_path)

    confidence_display = f"{confidence:.2f}%" if confidence is not None else "-"

    return {
        "time": timestamp,
        "name": name or "Unknown",
        "event": event,
        "status": status,
        "location": "Server Room",
        "confidence": confidence_display,
        "track_id": f"#{track_id}",
        "snapshot": snapshot,
    }


def _apply_filters(logs):
    """
    Terapkan semua filter dari widget di filters.py (dibaca lewat
    st.session_state) ke daftar log. Dipanggil SEKALI di get_filtered_logs(),
    dipakai bareng oleh tabel, tombol export CSV, dan panel detail --
    supaya ketiganya selalu menampilkan data yang konsisten.
    """

    search = st.session_state.get("audit_search", "") or ""
    search = search.strip().lower()

    event_filter = st.session_state.get("audit_event", "All Events")
    status_filter = st.session_state.get("audit_status", "All Status")
    user_filter = st.session_state.get("audit_user", "All Users")
    date_filter = st.session_state.get("audit_date")

    filtered = []

    for log in logs:

        if event_filter != "All Events" and log["event"] != event_filter:
            continue

        if status_filter != "All Status" and log["status"].title() != status_filter:
            continue

        if user_filter != "All Users" and log["name"] != user_filter:
            continue

        if date_filter is not None:
            log_date = str(log["time"])[:10]  # "YYYY-MM-DD HH:MM:SS" -> "YYYY-MM-DD"
            if log_date != str(date_filter):
                continue

        if search:
            haystack = f"{log['name']} {log['event']} {log['status']}".lower()
            if search not in haystack:
                continue

        filtered.append(log)

    return filtered


def get_filtered_logs():
    """
    Sumber data TUNGGAL untuk halaman Audit Log: query DB + terapkan
    filter yang lagi aktif. header.py (Export CSV), table.py (tabel),
    dan detail.py (panel kanan) semua pakai hasil dari fungsi ini,
    supaya tidak ada lagi data yang "gak sinkron" satu sama lain.
    """

    db = DatabaseService()
    logs = [_map_log(row) for row in db.get_logs()]

    return _apply_filters(logs)


def render_audit_table(logs):
    """
    Render tabel HTML dari `logs` yang sudah difilter (lihat
    get_filtered_logs()), lalu sediakan cara memilih baris agar detail
    panel di kanan ikut berubah sesuai baris yang dipilih.

    Return: dict log yang sedang dipilih (atau None kalau logs kosong).
    """

    if "selected_log_index" not in st.session_state:
        st.session_state.selected_log_index = 0

    if not logs:
        st.info("Tidak ada data yang cocok dengan filter saat ini.")
        return None

    if st.session_state.selected_log_index >= len(logs):
        st.session_state.selected_log_index = 0

    body_rows = ""

    for i, log in enumerate(logs):

        badge_class = "badge-success" if log["status"] == "AUTHORIZED" else "badge-danger"
        badge_label = log["status"].title()

        highlight = "background:#EFF6FF;" if i == st.session_state.selected_log_index else ""

        # PENTING: baris HTML di bawah ini SENGAJA tidak diberi indentasi
        # sama sekali. Kalau di-indent (misal ikut rapi sejajar kode
        # Python), Streamlit/Markdown akan menganggap baris berspasi 4+
        # di depan sebagai "code block", bukan HTML -- hasilnya malah
        # nampilin tag mentah kayak "</tbody></table>" sebagai teks biasa
        # di layar (bug yang sempat muncul).
        body_rows += (
            f'<tr style="{highlight}">'
            f'<td>{log["time"]}</td>'
            f'<td>{log["name"]}</td>'
            f'<td>{log["event"]}</td>'
            f'<td><span class="{badge_class}">{badge_label}</span></td>'
            f'<td>{log["location"]}</td>'
            f'<td>{log["confidence"]}</td>'
            f'<td>{log["track_id"]}</td>'
            f'</tr>'
        )

    table_html = (
        '<table class="custom-table">'
        '<thead><tr>'
        '<th>Time</th><th>User</th><th>Event</th><th>Status</th>'
        '<th>Location</th><th>Confidence</th><th>Track ID</th>'
        '</tr></thead>'
        f'<tbody>{body_rows}</tbody>'
        '</table>'
    )

    with st.container(border=True):

        st.markdown(table_html, unsafe_allow_html=True)

        st.caption("Pilih baris untuk melihat detail:")

        options = [
            f"{log['time']} - {log['name']} ({log['event']})"
            for log in logs
        ]

        selected_label = st.selectbox(
            "",
            options,
            index=st.session_state.selected_log_index,
            label_visibility="collapsed",
            key="audit_row_picker",
        )

        st.session_state.selected_log_index = options.index(selected_label)

    return logs[st.session_state.selected_log_index]
