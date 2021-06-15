# 基于Django的简单短视频分享平台
中国科学技术大学 2021春数据库实验
> ps:这实验真跟数据库没一点关系...完全是dlf老师突然异想天开出来的实验。
> 选到dlf的同学们尽早换班吧...

## 目录介绍
`/static`下是静态资源。包含js脚本,css文件和背景图片。`/static/dist/`下是bootstrap文件。
`/templates`下是html模板。包含所有界面。
`/TestModel`主要包含了模型定义`models.py`、处理http请求的`views.py`、解析url的`urls.py`
`/shortvids`下主要是项目的配置文件等，其中`/shortvids/settings.py`中`DATABASES`条目为数据库后端配置。
配置信息请根据实际情况调整

## 使用说明
在`manage.py`同级目录
```shell
$ python manage.py runserver
```
浏览器输入`127.0.0.1:8000`即可进入登录界面。

> ps:本项目在使用mysql数据库后端，python 3.7.10，django 2.2.5 以及chrome浏览器下可以成功运行。

更多其他信息请参考[django官中文档](https://docs.djangoproject.com/zh-hans)