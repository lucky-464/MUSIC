from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Albums)
admin.site.register(Musics)
admin.site.register(Artists)
admin.site.register(Customers)
admin.site.register(Playlist_songs)
admin.site.register(Playlists)
admin.site.register(Rating)

