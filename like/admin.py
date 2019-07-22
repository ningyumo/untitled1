from django.contrib import admin
from .models import Like


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'content_type', 'object_id', 'liker', 'create_time']
