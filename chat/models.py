from django.db import models
from django.contrib.auth.models import User

class DirectMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sent_dms', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_dms', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
