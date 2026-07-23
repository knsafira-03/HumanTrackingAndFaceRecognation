from datetime import datetime

from app.notification.whatsapp_service import WhatsAppService
from config.settings import WHATSAPP_TARGET


class NotificationManager:

    def __init__(self):

        self.whatsapp = WhatsAppService()

    def send_event(
        self,
        name,
        status,
        direction,
        snapshot_path=None
    ):

        now = datetime.now().strftime("%d %B %Y\n%H:%M:%S WIB")

        # ===============================
        # AUTHORIZED
        # ===============================

        if status == "AUTHORIZED":

            if direction == "MASUK":

                message = (
                    "🛡️ *SMART SERVER ROOM*\n\n"
                    "✅ *AUTHORIZED ACCESS*\n\n"
                    f"👤 Nama : *{name}*\n"
                    "🏢 Lokasi : *Server Room Diskominfotik*\n"
                    f"📍 Arah : *{direction}*\n\n"
                    f"🕒 Waktu :\n{now}\n\n"
                    "📊 Event berhasil dicatat ke sistem.\n\n"
                    "────────────────────\n"
                    "🤖 Smart Server Room Monitoring System"
                )

            else:

                message = (
                    "🛡️ *SMART SERVER ROOM*\n\n"
                    "🚪 *EXIT DETECTED*\n\n"
                    f"👤 Nama : *{name}*\n"
                    "🏢 Lokasi : *Server Room Diskominfotik*\n"
                    f"📍 Arah : *{direction}*\n\n"
                    f"🕒 Waktu :\n{now}\n\n"
                    "📊 Event berhasil dicatat ke sistem.\n\n"
                    "────────────────────\n"
                    "🤖 Smart Server Room Monitoring System"
                )

        # ===============================
        # UNAUTHORIZED
        # ===============================

        else:

            message = (
                "🚨 *SECURITY ALERT*\n\n"
                "❌ *UNAUTHORIZED ACCESS*\n\n"
                "👤 *Unknown Person*\n"
                "🏢 Lokasi : *Server Room Diskominfotik*\n"
                f"📍 Arah : *{direction}*\n\n"
                f"🕒 Waktu :\n{now}\n\n"
                "📸 Snapshot berhasil disimpan.\n\n"
                "🖥️ Silakan buka Dashboard\n"
                "untuk melihat foto lengkap.\n\n"
                "────────────────────\n"
                "🤖 Smart Server Room Monitoring System"
            )

        return self.whatsapp.send_message(
            WHATSAPP_TARGET,
            message
        )