# Generated by Django 2.2.3 on 2019-07-05 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myuser', '0004_verifycode'),
    ]

    operations = [
        migrations.AddField(
            model_name='verifycode',
            name='used',
            field=models.BooleanField(default=False),
        ),
    ]