import time

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.template import loader

from . import models


# Create your views here.
def get_all_vids(request):
    try:
        if request.session['is_login']:
            return HttpResponse('hello')
        else:
            return redirect('../login')
    except Exception as e:
        print(e)
        return redirect('../login')


def get_single_video(request, video_id):
    try:
        if request.session['is_login']:
            db_video = models.Video.get(id=video_id)
            template = loader.get_template('templates/singlevideo.html')
            context = {
                'video': db_video,
            }
            return HttpResponse(template.render(context, request))
        else:
            return redirect('../login')
    except Exception as e:
        print(e)
        return redirect('../login')


def upload(request):
    if request.session['is_login']:
        if request.method == "POST":
            user = request.session['user_id']
            title = request.POST['title']
            video = request.POST['video']
            db_video = models.Video(title=title, uploader_id=user, path="..", create_time=time.time())
            db_video.save()
        return redirect('../allvideos')
    else:
        return redirect('../login')



def log_in_page(request):
    if request.session.get('is_login', False):
        return redirect('../allvideos/')

    if (request.method == "POST") and 'username' in request.POST:
        user = request.POST['username']
        passwd = request.POST['password']
        # print(user)
        # true_name = request.POST['true_name']
        try:
            user_ins = models.User.create(user, passwd)
            user_ins.save()
            # request.session['is_login'] = True
            # request.session['user_id'] = user
            # request.session.set_expiry(120)
            return redirect('../login')
        except Exception as e:
            print(e)
            return redirect('../login')

    if request.method == "POST":
        user = request.POST['usernameIn']
        passwd = request.POST['passwordIn']
        try:
            db_user = models.User.objects.get(user_id=user)
            if db_user.password == passwd:
                request.session['is_login'] = True
                request.session['user_id'] = user
                request.session.set_expiry(120)
                return redirect('../allvideos/')
            else:
                return redirect('../login')
        except Exception as e:
            print(e)
            return redirect('../login')

    else:
        return render(request, 'login.html')


def logout(request):
    request.session.flush()
    return redirect('../login')
