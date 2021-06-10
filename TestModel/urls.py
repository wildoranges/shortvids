from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_all_vids, name='index'),
]
