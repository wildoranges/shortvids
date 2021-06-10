from django.db import models


class Video(models.Model):
    id = models.AutoField(primary_key=True) #TODO:
    title = models.CharField(max_length=30, default='untitled')
    create_time = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=256)
    cover_path = models.CharField(max_length=256)
    uploader_id = models.CharField(max_length=10) #TODO:FOREIGN KEY


class User(models.Model):
    user_id = models.CharField(max_length=10)
    password = models.CharField(max_length=10)


class Comment(models.Model):
    content = models.CharField(max_length=160)
    video_id = models.CharField(max_length=10, primary_key=True)#TODO:
    uploader_id = models.CharField(max_length=10)#TODO:

