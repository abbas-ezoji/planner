# Generated by Django 2.1.15 on 2020-05-07 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='airport',
            name='city',
        ),
        migrations.DeleteModel(
            name='airport',
        ),
    ]