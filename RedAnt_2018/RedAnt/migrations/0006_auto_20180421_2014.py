# Generated by Django 2.0.3 on 2018-04-21 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RedAnt', '0005_auto_20180421_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='ImagePath',
            field=models.CharField(max_length=20, null=True, verbose_name='图片'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='Name',
            field=models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='名称'),
        ),
    ]
