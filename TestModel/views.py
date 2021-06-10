from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View

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


def log_in_page(request):
    if request.session.get('is_login', False):
        return redirect('../allvideos/')

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
