from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View

from . import models


# Create your views here.
def vids(request):
    return redirect('/videos/index/')


def get_all_vids(request):
    try:
        if request.session['is_login']:
            return render(request, 'index.html')
        else:
            return redirect('../login/')
    except Exception as e:
        print(e)
        return redirect('../login/')


def login(request):
    if request.session.get('is_login', False):
        return redirect('../index/')

    if request.method == "POST":
        user = request.POST.get('username', None)
        passwd = request.POST.get('password', None)
        message = "所有字段都必须填写！"
        if user and passwd:
            user = user.strip()
            passwd = passwd.strip()
            try:
                db_user = models.User.objects.get(user_id=user)
                if db_user.password == passwd:
                    request.session['is_login'] = True
                    request.session['user_id'] = user
                    request.session.set_expiry(1800)
                    return redirect('../index/')
                else:
                    message = "密码不正确！"
            except Exception as e:
                print(e)
                message = "用户名不存在！"
        return render(request, 'login.html', {"message": message})

    else:
        return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        user = request.POST.get('username', None)
        passwd = request.POST.get('password', None)
        passwd2 = request.POST.get('password2', None)
        message = "所有字段都必须填写！"
        if user and passwd and passwd2:
            user = user.strip()
            passwd = passwd.strip()
            passwd2 = passwd2.strip()
            if passwd != passwd2:
                message = "两次密码不同，请重新输入！"
                return render(request, 'register.html', {"message": message})
            else:
                same_user = models.User.objects.filter(user_id=user)
                if same_user:
                    message = "该用户名已存在，请重新输入！"
                    return render(request, 'register.html', {"message": message})

                new_user = models.User.objects.create(user_id=user, password=passwd)
                new_user.save()
                request.session['is_login'] = True
                request.session['user_id'] = user
                request.session.set_expiry(1800)
                return redirect('../index/')

        return render(request, 'register.html', {"message": message})

    return render(request, 'register.html')


def logout(request):
    request.session.flush()
    return redirect('../login/')


def search(request):
    if not request.session.get('is_login', False):
        return redirect('../login/')

    else:
        return render(request, 'search.html')


def upload(request):
    if not request.session.get('is_login', False):
        return redirect('../login/')

    else:
        return render(request, 'upload.html')
