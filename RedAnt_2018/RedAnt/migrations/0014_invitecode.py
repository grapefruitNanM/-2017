# Generated by Django 2.0.3 on 2018-05-20 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RedAnt', '0013_auto_20180518_0903'),
    ]

    operations = [
        migrations.CreateModel(
            name='inviteCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('ddl', models.CharField(max_length=100)),
            ],
        ),
    ]
