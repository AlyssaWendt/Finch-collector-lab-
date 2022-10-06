from django.db import models
import time
from django.contrib.auth.models import User

# Create your models here.
class Finch(models.Model):

    name = models.CharField(max_length=150)
    img = models.CharField(max_length=500, default="avatar.png")
    bio = models.TextField(max_length=1000)
    verified_finch = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        
class Song(models.Model):

    title = models.CharField(max_length=150)
    length = models.IntegerField(default=0)
    finch = models.ForeignKey(Finch, on_delete=models.CASCADE, related_name="songs")

    def __str__(self):
        return self.title

    def get_length(self):
        return time.strftime("%-M:%S", time.gmtime(self.length))
    
class Playlist(models.Model):

    title = models.CharField(max_length=150)
    # this is going to create the many to many relationship and join table
    songs = models.ManyToManyField(Song)

    def __str__(self):
        return self.title


    

