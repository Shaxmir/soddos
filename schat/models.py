from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Message(models.Model):
    login = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages', verbose_name='Отправитель')
    message = models.TextField(max_length=500, verbose_name='Текст сообщения')
    create_dt = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')