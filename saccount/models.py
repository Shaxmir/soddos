import os
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


# Create your models here.
class ProfileImg(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_img')
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpg', verbose_name='Аватар')

    def save(self, *args, **kwargs):
        # Если объект уже существует
        if self.pk:
            old_avatar = ProfileImg.objects.get(pk=self.pk).avatar
            # Проверяем, изменился ли файл аватара
            if old_avatar and old_avatar != self.avatar:
                old_avatar.delete(save=False)  # Удаляем старый файл аватара

        # Присваиваем новое имя файлу
        if self.avatar:
            ext = os.path.splitext(self.avatar.name)[-1].lower()  # Расширение файла
            new_name = f"{self.user.username}_{now().strftime('%Y%m%d%H%M%S')}{ext}"
            self.avatar.name = new_name

        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.user.username} Profile'

