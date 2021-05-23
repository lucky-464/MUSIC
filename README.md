# MUSIC
This project is completely front end independent.
Every functionality in it is implemented using API endpoints.

api/urls.py : has defined url paths for each functionality 

'Music List': '/musics/',
'Playlists' : '/playlist/',
'Playlist Songs' : '/playlistsongs/',
'User Specific Playlist':'/userplaylists/<str:pk>/',
'Delete Specific Playlist': '/deleteplaylist/<str:pk>/',
'Search Song Based on Tiltle Album Genre Artist': '/searchsong/',
'Recommended song based on user id': '/recommendsong/<str:pk>/'

CURD functionality has been implemented using the Rest framework
