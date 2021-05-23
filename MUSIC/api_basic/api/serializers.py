from rest_framework import serializers
from api_basic.models import Musics, Albums, Artists, Customers, Playlists, Playlist_songs, Rating

class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Musics
        fields = "__all__"


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Albums
        fields = "__all__"

class ArtistsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artists
        fields = "__all__"

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = "__all__"


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlists
        fields = "__all__"

class PLaylistSongsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist_songs
        fields = "__all__"

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = "__all__"