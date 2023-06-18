import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.urls import reverse
from pharmacist.models import Notification



class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.group_name = f"user_{self.user_id}"
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        await self.get_notification_data({'user_id': self.user_id})



    async def get_notification_data(self, event):
        user_id = event['user_id']
        notification_count = await Notification.get_unread_notification_count(user_id)
        notifications = await Notification.get_unread_notifications(user_id)
        data = {
            "notification_count": notification_count,
            "notifications": []
        }


        for notification in notifications:
            url = reverse("doctor:appointments") if notification.title == "New Appointment" else reverse("doctor:prescriptions")
            data["notifications"].append({
                "title": notification.title,
                "content": notification.content,
                "url": url
            })

        json_data = json.dumps(data)
        await self.send(text_data=json_data)
