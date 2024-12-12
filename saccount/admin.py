from django.contrib import admin
from saccount.models import ProfileImg


# Register your models here.
@admin.register(ProfileImg)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar')