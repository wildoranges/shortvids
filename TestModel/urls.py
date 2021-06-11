from django.urls import path
from django.urls import re_path
from django.views.static import serve
from shortvids import settings

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('index/', views.get_all_vids, name='index'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('search/', views.search, name='search'),
    path('upload/', views.upload, name='upload'),

    # path('<int:video_id>/', views.get_single_video, name='single_video'),
    path('<int:video_id>/', views.get_single_video, name='single_video'),
    re_path('media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),
    path('', views.vids, name='main')

]
