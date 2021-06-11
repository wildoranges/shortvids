from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.template import loader

from django.http import Http404

from datetime import datetime
import os
from shortvids import settings


from . import models


# Create your views here.
def vids(request):
    return redirect('/videos/index/')


def get_all_vids(request):
    if request.session.get('is_login', False):
        all_vids = models.Video.objects.all()
        return render(request,'index.html',{'ref':all_vids,'MEDIA_URL':settings.MEDIA_URL})

    else:
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


support_vids = ['.mp4', '.webm', '.ogg']
support_imgs = ['.jpg', '.png', '.jpeg', '.bmp', '.webp']


def upload(request):
    if request.session.get('is_login', False):
        if request.method == "POST":
            userid = request.session['user_id']
            user = models.User.objects.get(user_id=userid)
            title = request.POST['title']
            video = request.FILES['video']
            cover = request.FILES['cover']
            now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            vid_name, vid_ext = os.path.splitext(os.path.split(video.name)[1])
            print("vid_name", vid_name)
            cov_name, cov_ext = os.path.splitext(os.path.split(cover.name)[1])
            print("cov_name", cov_name)
            if vid_ext.lower() not in support_vids:
                message = "不支持的视频类型，仅支持.mp4,.webm,.ogg"
                return render(request, 'upload.html', {"message": message})
            if cov_ext.lower() not in support_imgs:
                message = "不支持的图片类型，仅支持.jpg,.png,.jpeg,.bmp,.webp"
                return render(request, 'upload.html', {"message": message})
            video.name = userid + '_' + vid_name + '_' + now + vid_ext
            cover.name = userid + '_' + cov_name + '_' + now + cov_ext
            vid_file_path = os.path.join('videos', video.name)
            cov_file_path = os.path.join('images', cover.name)
            db_video = models.Video.objects.create(title=title, path=vid_file_path, vid=video, cover=cover,
                                                   cover_path=cov_file_path, uploader_id=user)
            db_video.save()
            return redirect('../index')

        return render(request, 'upload.html')
    else:
        return redirect('../login')


def get_single_video(request, video_id):
    if request.session['is_login']:
        try:
            db_video = models.Video.objects.get(id=video_id)
            db_comment = models.Comment.objects.filter(video_id=db_video)
            print(db_video.path)
            template = loader.get_template('singlevideo.html')
            context = {
                'video': db_video,
                'comments': db_comment,
            }
            # print(db_video.video.cover.url)
            if request.method == "POST":
                net_content = request.POST['new_comment']
                user = db_video.uploader_id
                db_new_com = models.Comment.objects.create(content=net_content, video_id=db_video, uploader_id=user)
                db_new_com.save()

            return HttpResponse(template.render(context, request))
        except Exception as e:
            print(e)
            raise Http404("video not found")
            return redirect('../allvideos/')
    else:
        return redirect('../login')

