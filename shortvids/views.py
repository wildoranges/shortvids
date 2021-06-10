from django.http import HttpResponse
from django.shortcuts import render


def hello(request):
    usernamein = request.POST['']