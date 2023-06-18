from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from patient.models import Prescription
from pharmacist.models import Notification
from accounts.models import CustomUser

@receiver(post_save, sender=Prescription)
def prescription_saved(sender, instance, created, **kwargs):
    user = CustomUser.objects.get(id=instance.doctor.user.id)
    if created:
        #! pharmacist notification
        # Notification.objects.create(user=user, title="New Prescription", content="You have a new Prescription")
        pass
    else:
        if instance.status == "rejected":
            Notification.objects.create(user=user, title="Rejected Prescription", content="Prescription has been rejected")
        elif instance.status == "approved":
            Notification.objects.create(user=user, title="Approved Prescription", content="Prescription has been approved")

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