from app.notification.whatsapp_service import WhatsAppService

wa = WhatsAppService()

result = wa.send_message(
    target="6281378946896",
    message="🚀 Test dari Smart Server Room"
)

print(result)