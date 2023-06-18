from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from patient.models import Request
from pharmacist.models import Notification
from accounts.models import CustomUser

@receiver(post_save, sender=Request)
def request_saved(sender, instance, created, **kwargs):
    user = CustomUser.objects.get(id=instance.doctor.user.id)
    if created:
        Notification.objects.create(user=user, title="New Appointment", content="You have a new appointment")
        channel_layer = get_channel_layer()
        group_name = f"user_{user.id}"
        try:
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    "type": "get_notification_data",
                    "user_id": user.id,
                }
            )
        except:
            pass