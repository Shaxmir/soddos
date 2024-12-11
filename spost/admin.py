from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'create_dt', 'update_dt')  # Поля для отображения в списке
    list_filter = ('author', 'create_dt')  # Фильтрация по автору и дате создания
    search_fields = ('title', 'content')  # Поля для поиска
    ordering = ('-create_dt',)  # Сортировка по дате создания (в обратном порядке)

# Регистрация модели и класса админки
admin.site.register(Post, PostAdmin)