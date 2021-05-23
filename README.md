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

Initially the database is created by the system by creating different albums of artists, genres. 
User can add songs with title, artists(can be more then one), genre to there playlists and rate them. A song could be in multiple playlists same goes with the arists its a many to many relation.
Based on user playlist system Recommended them songs by extracting their genre, taste, there favourite artists and albums they like and suggest them the songs keeping these things into consideration

CURD functionality has been implemented using the Rest framework, and CURD operations could be done using postman or could be directly through the server where  specific things could be seen using their url paths (get operation), upload new song, playlists etc using post operation and update and delete them using put operation. 

