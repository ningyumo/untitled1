# Generated by Django 2.2.3 on 2019-07-04 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myuser', '0002_auto_20190704_1600'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='location',
        ),
    ]