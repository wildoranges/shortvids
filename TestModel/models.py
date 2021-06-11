from django.db import models


class User(models.Model):
    user_id = models.CharField(max_length=10, primary_key=True)
    password = models.CharField(max_length=10)


class Video(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30, default='untitled')
    create_time = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=256)
    vid = models.FileField(verbose_name="视频")
    cover_path = models.CharField(max_length=256)
    cover = models.ImageField(verbose_name="封面")
    uploader_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.CharField(max_length=160, default='no comment')
    video_id = models.ForeignKey(Video, on_delete=models.CASCADE)
    uploader_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
