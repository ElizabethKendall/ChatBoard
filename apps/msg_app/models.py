from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.db import models
from ..user_app.models import User

# Create your models here.

def validateLengthGreaterThan15(value):
    if len(value) < 16:
        raise ValidationError(
            'Your content must be at least 15 characters'
        )

class Message(models.Model):
    content = models.CharField(max_length=1000, default="", validators=[validateLengthGreaterThan15])
    author = models.ForeignKey(User, related_name="authored_messages") 
    receiver = models.ForeignKey(User, related_name="messages_received")       
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

class Comment(models.Model):
    content = models.CharField(max_length=1000, default="", validators=[validateLengthGreaterThan15])
    author = models.ForeignKey(User, related_name="authored_comments")
    message = models.ForeignKey(Message, related_name="comments_for_message")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

