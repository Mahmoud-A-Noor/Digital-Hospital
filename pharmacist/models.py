from django.db import models
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async

# Create your models here.


class Pharmacist(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.user.email
    

class Notification(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(blank=True, auto_now_add=True)

    @staticmethod
    async def get_unread_notification_count(user_id):
        query = Notification.objects.filter(user__id=user_id, is_read=False)
        count = await sync_to_async(query.count)()
        return count

    @staticmethod
    async def get_unread_notifications(user_id):
        query = Notification.objects.filter(user__id=user_id, is_read=False).order_by("created_at")
        notifications = await sync_to_async(list)(query)
        return notifications

    @staticmethod
    def mark_all_as_read(user_id):
        notifications = Notification.objects.filter(user__id=user_id, is_read=False)
        notifications.update(is_read=True)