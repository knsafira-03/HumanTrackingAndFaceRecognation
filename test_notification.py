from app.notification.notification_manager import NotificationManager

notification = NotificationManager()

result = notification.send_event(
    target="6281378946896",
    name="Khalisa",
    status="AUTHORIZED",
    direction="MASUK"
)

print(result)