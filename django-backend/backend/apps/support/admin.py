from django.contrib import admin

from apps.support import models


@admin.register(models.SupportMessage)
class SupportMessageAdmin(admin.ModelAdmin):
    list_display = (
        'email', 'status', 'created',
    )
    ordering = (
        'status',
    )
    list_filter = (
        'status',
    )
    search_fields = ('id', 'email', 'status', 'created')
