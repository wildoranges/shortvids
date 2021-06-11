from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('index/', views.get_all_vids, name='index'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('search/', views.search, name='search'),
    path('upload/', views.upload, name='upload'),
    path('', views.vids, name='main')
]
