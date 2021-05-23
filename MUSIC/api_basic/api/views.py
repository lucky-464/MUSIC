from django.http import response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from api_basic.models import Albums, Artists, Customers, Musics, Playlist_songs, Playlists, Rating
from .serializers import MusicSerializer, PLaylistSongsSerializer, PlaylistSerializer, RatingSerializer
import re
from collections import OrderedDict

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Music List': '/musics/',
        'Playlists' : '/playlist/',
        'Playlist Songs' : '/playlistsongs/',
        'User Specific Playlist':'/userplaylists/<str:pk>/',
        'Delete Specific Playlist': '/deleteplaylist/<str:pk>/',
        'Search Song Based on Tiltle Album Genre Artist': '/searchsong/',
        'Recommended song based on user id': '/recommendsong/<str:pk>/'
    }
    # response = MusicListApiView.as_view()(request=request._request).data
    return Response(api_urls)

@api_view(['GET'])
def userPlaylistOverview(request, pk):
    # user = get_object_or_404(Customers, pk)
    user = Customers.objects.get(id = pk)
    user_playlists = user.playlists_set.all()
    
    data = list()
    for playlist in user_playlists:
        playlist_song_obj = Playlist_songs.objects.filter(playlist_id = playlist.id)
        serializer = PLaylistSongsSerializer(playlist_song_obj, many = True)
        data.extend(serializer.data)

    return Response(data)
    
        

class MusicListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        todos = Musics.objects.all()
        serializer = MusicSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        data = {
            'title': request.data.get('title'), 
            'artists': request.data.get('artists'), 
            'genre': request.data.get('genre'),
            'album': request.data.get('album'),
            
        }
        serializer = MusicSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PlaylistApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        todos = Playlists.objects.all()
        serializer = PlaylistSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        data = {
            'name': request.data.get('name'), 
            'customer_id': request.data.get('customer_id')
            
        }
        serializer = PlaylistSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):

        data = {
            'name': request.data.get('name'),
            'new_name' : request.data.get('new_name'), 
            'customer_id': request.data.get('customer_id')
            
        }
        new_data = {'name' : data['new_name'], 'customer_id': data['customer_id']}
        playlist_obj = Playlists.objects.get(name = data['name'])

        serializer = PlaylistSerializer(instance = playlist_obj,data=new_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','DELETE'])
def deletePlaylist(request,pk):
    playlist = Playlists.objects.get(id = pk)
    if request.method == 'GET':
        return Response(PlaylistSerializer(playlist).data)
    
    playlist.delete()
    return Response('Item got deleted')


class PlaylistSongApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        todos = Playlist_songs.objects.all()
        serializer = PLaylistSongsSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        data = {
            'playlist_id': request.data.get('playlist_id'), 
            'music_id': request.data.get('music_id')
            
        }
        # playlist_id = Playlists.objects.get(id = data['playlist_id'])
        serializer = PLaylistSongsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, *args, **kwargs):
            '''
            Create the Todo with given todo data
            '''
            data = {
                'playlist_id': request.data.get('playlist_id'), 
                'music_id': request.data.get('music_id')
                
            }
            # playlist_id = Playlists.objects.get(id = data['playlist_id'])
            Playlist_song_id = Playlist_songs.objects.get(playlist_id = data['playlist_id'])
            serializer = PLaylistSongsSerializer(instance =Playlist_song_id ,data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def searchsong(request):

    if request.method == 'POST':
        
        search_result = dict()
        music_obj = Musics.objects.all()
        artists_obj = Artists.objects.all()
        album_obj =Albums.objects.all()
        data = request.data
        
        # search by title match
        if(data['title'] !="" and data['title'] is not None):
            search_result['title'] = []
            for music in music_obj:
                if( re.search(data.get('title'), music.title, re.IGNORECASE)):
                    search_result['title'].append(MusicSerializer(music).data)
       
        # search by artist match
        if(data['artist'] !="" and data['artist'] is not None):
            search_result['artist'] = []
            for artist in artists_obj:
                if( re.search(data.get('artist'), artist.name, re.IGNORECASE)):
                    music = Musics.objects.filter(artists = artist.id)
                    search_result['artist'].extend(MusicSerializer(music, many =True).data)
        
        # search by genere match
        if(data['genre'] !="" and data['genre'] is not None):
            search_result['genre'] = []
            for music in music_obj:
                if( re.search(data.get('genre'), music.genre, re.IGNORECASE)):
                    search_result['genre'].append(MusicSerializer(music).data)
       
        # search by album match
        if(data['album'] !="" and data['album'] is not None):
            search_result['album'] = []
            for album in album_obj:
                if( re.search(data.get('album'), album.name, re.IGNORECASE)):
                    music = Musics.objects.filter(album = album.id)
                    search_result['album'].extend(MusicSerializer(music, many =True).data)

        return Response(search_result)

    search_format = {
        'title':"",
        "artist":"",
        "genre":"",
        "album" : ""
    }
    return Response(search_format)

@api_view(['GET'])
def recommendSong(request, pk):

    user = Customers.objects.get(id = pk)
    user_playlists = user.playlists_set.all()
    result_list = []
    data = list()
    for playlist in user_playlists:
        playlist_song_obj = Playlist_songs.objects.filter(playlist_id = playlist.id)
        serializer = PLaylistSongsSerializer(playlist_song_obj, many = True)
        data.extend(serializer.data)

    # got list of dictionaries of playlist with song ids

    
    collected_music_id = []
    for item in data:
        collected_music_id.extend(item['music_id'])
    
    
    # removing duplicates
    collected_music_id = list(OrderedDict.fromkeys(collected_music_id))
    
    collected_music_genre = []
    collected_music_artists = []
    collected_music_album = []

    for id in collected_music_id:
        if Musics.objects.get(id = id).genre not in collected_music_genre:
            collected_music_genre.append(Musics.objects.get(id = id).genre)
        
        if Musics.objects.get(id = id).album.name not in collected_music_album:
            collected_music_album.append(Musics.objects.get(id = id).album.name)
        
        list_artists = list(Musics.objects.get(id = id).artists.all().order_by('name').values_list('name',flat =True).distinct())
        collected_music_artists.extend(list_artists)


    collected_music_artists = list(OrderedDict.fromkeys(collected_music_artists))   

    all_musics = Musics.objects.all()
    
    for music in all_musics:
        if music.id not in collected_music_id:
            # print(music.artists.all())
            current_artists = list(music.artists.all().order_by('name').values_list('name',flat =True).distinct())
            if music.album.name in collected_music_album or \
                 music.genre in collected_music_genre or \
                     any(item in current_artists for item in collected_music_artists):
                
                result_list.append(MusicSerializer(music).data)
    return Response(result_list)


class RatingApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        todos = Rating.objects.all()
        serializer = RatingSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        data = {
            'rating': request.data.get('rating'),
            'music_id': request.data.get('music_id'), 
            'customer_id': request.data.get('customer_id')
            
        }
        serializer = RatingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):

        data = {
            'rating': request.data.get('rating'),
            'music_id': request.data.get('music_id'), 
            'customer_id': request.data.get('customer_id')
            
        }
        
        rating_obj = Rating.objects.get(customer_id = data['customer_id'])

        serializer = RatingSerializer(instance = rating_obj,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def randomRecommendation(request):
    pass

                     

