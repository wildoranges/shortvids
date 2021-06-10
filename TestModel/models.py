from django.db import models
from django.db.models.deletion import CASCADE


class Video(models.Model):
    id = models.AutoField(primary_key=True) #TODO:
    title = models.CharField(max_length=30, default='untitled')
    create_time = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=256)
    cover_path = models.CharField(max_length=256)
    # uploader_id = models.CharField(max_length=10) #TODO:FOREIGN KEY
    uploader_id = models.ForeignKey('User', on_delete=CASCADE)

    def __str__(self) -> str:
        return self.path

class User(models.Model):
    user_id = models.CharField(max_length=10, primary_key=True)
    password = models.CharField(max_length=10)
    # video = models.ForeignKey('Video', on_delete=CASCADE)

    def __str__(self) -> str:
        return self.user_id

class Comment(models.Model):
    content = models.CharField(max_length=160)
    video_id = models.CharField(max_length=10)#TODO:
    # uploader_id = models.CharField(max_length=10)#TODO:
    uploader_id = models.ForeignKey('User', on_delete=CASCADE)

    def __str__(self) -> str:
        return self.content
