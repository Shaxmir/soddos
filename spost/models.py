from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_post',
        verbose_name='Автор поста'
    )
    title = models.CharField(
        max_length=200,
        blank=False,
        verbose_name='Заголовок'
    )
    content = models.TextField(
        blank=False,
        verbose_name='Текст поста'
    )
    create_dt = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    update_dt = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения'
    )

    def get_absolute_url(self):
        return reverse('post_detali', kwargs={'id' : self.id})

    def __str__(self):
        """
            Отображение в админке
        """
        return f'Пост: {self.title}. Автор {self.author}'

