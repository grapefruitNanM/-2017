# Generated by Django 2.0.3 on 2018-06-16 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RedAnt', '0031_auto_20180615_2320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='ImagePath',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
