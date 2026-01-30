from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="emails")
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }