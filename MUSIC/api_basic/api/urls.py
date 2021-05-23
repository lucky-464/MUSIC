from django.conf.urls import url
from django.urls import path, include
from .views import (
    MusicListApiView,apiOverview,PlaylistApiView, userPlaylistOverview,
    PlaylistSongApiView,deletePlaylist, searchsong, recommendSong, RatingApiView
)

urlpatterns = [
    path('', apiOverview, name="api-overview"),
    path('musics/', MusicListApiView.as_view()),
    path('playlist/', PlaylistApiView.as_view()),
    path('playlistsongs/', PlaylistSongApiView.as_view()),
    path('rating/', RatingApiView.as_view()),

    path('userplaylists/<str:pk>',userPlaylistOverview, name='user-playlist'),
    path('deleteplaylist/<str:pk>',deletePlaylist, name='deleteplaylist'),
    path('searchsong/',searchsong, name='searchsong'),
    path('recommendsong/<str:pk>',recommendSong, name='recommend-user-song'),
]