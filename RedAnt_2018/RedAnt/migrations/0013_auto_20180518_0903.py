# Generated by Django 2.0.3 on 2018-05-18 01:03

import RedAnt.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RedAnt', '0012_auto_20180518_0057'),
    ]

    operations = [
        migrations.AddField(
            model_name='learningresources',
            name='teamName',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='learningresources',
            name='fileField',
            field=models.FileField(upload_to=RedAnt.models.get_upload_path),
        ),
    ]
