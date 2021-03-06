# Generated by Django 2.2.5 on 2021-06-10 11:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(default='untitled', max_length=30)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('path', models.CharField(max_length=256)),
                ('cover_path', models.CharField(max_length=256)),
                ('uploader_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TestModel.User')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(default='no comment', max_length=160)),
                ('uploader_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TestModel.User')),
                ('video_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TestModel.Video')),
            ],
        ),
    ]
