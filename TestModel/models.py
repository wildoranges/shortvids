from django.db import models
import os
from shortvids import settings


class User(models.Model):
    user_id = models.CharField(max_length=10, primary_key=True)
    password = models.CharField(max_length=10)
    friends = models.ManyToManyField("self", symmetrical=False)

    def __str__(self):
        return self.user_id


class Video(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30, default='untitled')
    create_time = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=256)
    vid = models.FileField(verbose_name="视频", default='settings.MEDIA_ROOT/videos/default.mp4', \
                           upload_to=os.path.join(settings.MEDIA_ROOT, 'videos'))
    cover_path = models.CharField(max_length=256)
    cover = models.ImageField(verbose_name="封面", default='settings.MEDIA_ROOT/images/default.png', \
                              upload_to=os.path.join(settings.MEDIA_ROOT, 'images'))
    uploader_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.CharField(max_length=160, default='no comment')
    video_id = models.ForeignKey(Video, on_delete=models.CASCADE)
    uploader_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
