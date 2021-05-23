from django.db import models
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Musics(models.Model):
    title = models.CharField(max_length=500)
    artists = models.ManyToManyField('Artists')
    genre = models.CharField(max_length=200)
    album = models.ForeignKey('Albums', on_delete=models.CASCADE)

    class META:
        ordering = "id"


    def __str__(self):
        return self.title

class Albums(models.Model):
    name = models.CharField(max_length=400)
    artist_id = models.ManyToManyField('Artists')

    def __str__(self):
        return self.name


class Artists(models.Model):
    name = models.CharField(max_length=400)    
    def __str__(self):
        return self.name

class Customers(models.Model):
    name = models.CharField(max_length=200)
    email  = models.EmailField(max_length=200)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Playlists(models.Model):
    name = models.CharField(max_length=200)
    customer_id = models.ForeignKey(Customers, on_delete= models.CASCADE)



    def __str__(self):
        return self.name    

class Playlist_songs(models.Model):
    playlist_id = models.ForeignKey(Playlists, on_delete= models.CASCADE)
    music_id = models.ManyToManyField('Musics')

class Rating(models.Model):
    RATING_CHOICES = (
                        ("1", "1"),
                        ("2", "2"),
                        ("3", "3"),
                        ("4", "4"),
                        ("5", "5"),
                        )  
    rating =models.CharField(
        max_length = 20,
        choices = RATING_CHOICES,
        default = '1'
        )
    music_id = models.ForeignKey(Musics,on_delete= models.CASCADE)
    customer_id = models.ForeignKey(Customers, on_delete= models.CASCADE)

    def __str__(self) :
        return self.rating


