# Generated by Django 2.2.3 on 2019-07-04 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myuser', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(choices=[(None, '请选择地址'), ('浙江', (('杭州', '杭州'), ('宁波', '宁波')))], max_length=100),
        ),
    ]