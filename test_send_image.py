from app.notification.whatsapp_service import WhatsAppService
from config.settings import WHATSAPP_TARGET

wa = WhatsAppService()

result = wa.send_image(
    target=WHATSAPP_TARGET,
    message="📷 Tes kirim snapshot dari Smart Server Room",
    image_path="snapshots/20260723_104642_unknown_keluar.jpg"
)

print(result)