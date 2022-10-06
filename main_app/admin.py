from django.contrib import admin
from .models import Finch, Song, Playlist
# Register your models here.

admin.site.register(Finch)
admin.site.register(Song)
admin.site.register(Playlist)

