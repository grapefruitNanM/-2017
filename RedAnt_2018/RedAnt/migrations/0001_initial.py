# Generated by Django 2.0.3 on 2018-04-21 09:29

import DjangoUeditor.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('Name', DjangoUeditor.models.UEditorField(primary_key=True, serialize=False, verbose_name='日志标题')),
                ('ImagePath', DjangoUeditor.models.UEditorField(verbose_name='封面图片')),
                ('Content', DjangoUeditor.models.UEditorField(verbose_name='内容')),
                ('modify_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='LearningResources',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=20)),
                ('Introduction', DjangoUeditor.models.UEditorField()),
            ],
        ),
        migrations.AddField(
            model_name='learningresources',
            name='Team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RedAnt.ProjectTeam'),
        ),
        migrations.AddField(
            model_name='blog',
            name='Team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='RedAnt.ProjectTeam'),
        ),
    ]