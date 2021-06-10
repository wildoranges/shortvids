from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.log_in_page, name='login'),
    path('allvideos/', views.get_all_vids, name='allvideos'),
    path('upload/', views.uplaod, name='upload'),
    path('logout/', views.logout, name='logout'),
    path('<int:id>/', views.get_single_video, name='single_video')
]
