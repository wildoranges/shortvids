from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.template import loader
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
        return render(request, 'index.html', {'ref': all_vids, 'MEDIA_URL': settings.MEDIA_URL})

    else:
        return redirect('../login/')


def user(request):
    if not request.session.get('is_login', False):
        return redirect('../login/')
    else:
        db_user = models.User.objects.all()
        return render(request, 'user.html', {'users': db_user})


def get_single_user(request, user_id):
    if not request.session.get('is_login', False):
        return redirect('../login/')

    else:
        try:
            db_user = models.User.objects.get(user_id=user_id)
            db_video = models.Video.objects.filter(uploader_id=db_user)
            return render(request, 'singleuser.html', {'user': db_user, 'videos': db_video})
        except Exception as e:
            print(e)
            return render(request, 'reminder.html', {'message': "没有相关用户"})


def login(request):
    if request.session.get('is_login', False):
        return redirect('../index/')

    if request.method == "POST":
        cur_user = request.POST.get('username', None)
        passwd = request.POST.get('password', None)
        message = "所有字段都必须填写！"
        if cur_user and passwd:
            cur_user = cur_user.strip()
            passwd = passwd.strip()
            try:
                db_user = models.User.objects.get(user_id=cur_user)
                if db_user.password == passwd:
                    request.session['is_login'] = True
                    request.session['user_id'] = cur_user
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
        cur_user = request.POST.get('username', None)
        passwd = request.POST.get('password', None)
        passwd2 = request.POST.get('password2', None)
        message = "所有字段都必须填写！"
        if cur_user and passwd and passwd2:
            cur_user = cur_user.strip()
            if len(cur_user) > 10:
                message = "用户名长度不能超过10，请重新输入！"
                return render(request, 'register.html', {"message": message})
            passwd = passwd.strip()
            passwd2 = passwd2.strip()
            if passwd != passwd2:
                message = "两次密码不同，请重新输入！"
                return render(request, 'register.html', {"message": message})
            if len(passwd) > 10:
                message = "密码长度不能超过10,请重新输入！"
                return render(request, 'register.html', {"message": message})
            else:
                same_user = models.User.objects.filter(user_id=cur_user)
                if same_user:
                    message = "该用户名已存在，请重新输入！"
                    return render(request, 'register.html', {"message": message})

                new_user = models.User.objects.create(user_id=cur_user, password=passwd)
                new_user.save()
                request.session['is_login'] = True
                request.session['user_id'] = cur_user
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
        if request.method == "POST":
            sel = request.POST.get("searchSelect", "videos")
            query = request.POST.get("searchInput", None)
            if sel == "videos" and query:
                db_videos = models.Video.objects.filter(title__icontains=query)
                if len(db_videos) == 0:
                    context = {
                        "message": "没有更多的视频!"
                    }
                    return render(request, 'reminder.html', context)
                return render(request, 'index.html', {'ref': db_videos, 'MEDIA_URL': settings.MEDIA_URL})
            elif sel == "users" and query:
                db_user = models.User.objects.filter(user_id__icontains=query)
                if len(db_user) == 0:
                    context = {
                        'message': "没有相关用户!"
                    }
                    return render(request, 'reminder.html', context)
                return render(request, 'user.html', {'users': db_user})
            return render(request, "search.html")
        return render(request, 'search.html')


support_vids = ['.mp4', '.webm', '.ogg']
support_imgs = ['.jpg', '.png', '.jpeg', '.bmp', '.webp']


def upload(request):
    if request.session.get('is_login', False):
        if request.method == "POST":
            userid = request.session['user_id']
            cur_user = models.User.objects.get(user_id=userid)
            title = request.POST['title']
            if len(title) > 30:
                message = "标题长度不能超过30！"
                return render(request, 'upload.html', {"message": message})
            video = request.FILES['video']
            cover = request.FILES['cover']
            now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            vid_name, vid_ext = os.path.splitext(os.path.split(video.name)[1])
            # print("vid_name", vid_name)
            cov_name, cov_ext = os.path.splitext(os.path.split(cover.name)[1])
            # print("cov_name", cov_name)
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
            if len(vid_file_path) > 256 or len(cov_file_path) > 256:
                message = "文件名过长！"
                return render(request, 'upload.html', {"message": message})
            db_video = models.Video.objects.create(title=title, path=vid_file_path, vid=video, cover=cover,
                                                   cover_path=cov_file_path, uploader_id=cur_user)
            db_video.save()
            return redirect('../index')

        return render(request, 'upload.html')
    else:
        return redirect('../login')


def get_single_video(request, video_id):
    if request.session.get('is_login', False):
        try:
            db_video = models.Video.objects.get(id=video_id)
            db_comment = models.Comment.objects.filter(video_id=db_video)
            # print(db_video.path)
            cur_url = request.build_absolute_uri()
            # print(cur_url)
            template = loader.get_template('singlevideo.html')
            context = {
                'video': db_video,
                'comments': db_comment,
                'url': cur_url
            }
            # print(db_video.video.cover.url)
            # to display in chrome the video need to be mp4 H264 use online convert
            if request.method == "POST":
                comment = request.POST['new_comment']
                # print(comment)
                # print(len(comment))
                if (len(comment) > 0) & (len(comment) <= 160):
                    print("save comment")
                    db_user = models.User.objects.get(user_id=request.session['user_id'])
                    db_new_com = models.Comment.objects.create(content=comment, video_id=db_video, uploader_id=db_user)
                    db_new_com.save()
                elif len(comment) <= 0:
                    context['errorMes'] = "留言不得为空"
                else:
                    context['errorMes'] = "留言不得超过160"
            return HttpResponse(template.render(context, request))
        except Exception as e:
            print(e)
            context = {
                "message": "404 Not Found"
            }
            return render(request, "reminder.html", context, status=404)
    else:
        return redirect('../login')


def dynamic(request):
    if request.session.get('is_login', False):
        cur_id = request.session.get('user_id', None)
        cur_user = models.User.objects.get(user_id=cur_id)
        friends = cur_user.friends.all()
        video_set = models.Video.objects.none()
        for cur_user in friends:
            videos = models.Video.objects.filter(uploader_id=cur_user)
            video_set = video_set | videos
        if len(video_set) <= 0:
            message = '没有更多的动态！'
            return render(request, "reminder.html", {"message": message})
        context = {
            "ref": video_set,
            "MEDIA_URL": settings.MEDIA_URL
        }
        return render(request, 'dynamic.html', context)
    else:
        return redirect('../login')
