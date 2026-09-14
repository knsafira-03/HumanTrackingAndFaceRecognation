import io
import csv
import streamlit as st


def render_audit_header(logs):
    """
    logs: hasil dari get_filtered_logs() -- CSV yang di-export akan
    mengikuti filter yang lagi aktif di layar, bukan semua data mentah.
    """

    left, right = st.columns([6, 1])

    with left:

        st.markdown("## 📋 Audit Log")
        st.caption("All system access and detection events")

    with right:

        st.write("")
        st.write("")

        csv_buffer = io.StringIO()

        if logs:
            writer = csv.DictWriter(
                csv_buffer,
                fieldnames=["time", "name", "event", "status", "location", "confidence", "track_id"]
            )
            writer.writeheader()
            for log in logs:
                writer.writerow({k: log[k] for k in writer.fieldnames})

        st.download_button(
            "⬇ Export CSV",
            data=csv_buffer.getvalue(),
            file_name="audit_log.csv",
            mime="text/csv",
            use_container_width=True,
            disabled=not logs,
            key="export_csv",
        )
