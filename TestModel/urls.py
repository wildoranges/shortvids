from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.log_in_page, name='login'),
    path('allvideos/', views.get_all_vids, name='allvideos'),
    path('logout/', views.logout, name='logout')
]
