# Generated by Django 2.2.3 on 2019-07-11 02:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='is_first_comment',
        ),
    ]
