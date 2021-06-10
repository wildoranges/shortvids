from django.contrib import admin
from . import models

from .models import Video
from .models import *
# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Video)
admin.site.register(models.Comment)
