from django.contrib import admin
from .models import MediawikiUser


class MediawikiUserAdmin(admin.ModelAdmin):
        list_display = ('user', 'username')
        search_fields = ('user__username', 'username')

admin.site.register(MediawikiUser, MediawikiUserAdmin)
