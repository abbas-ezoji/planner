# Generated by Django 2.1.15 on 2020-03-24 15:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0011_attractions_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attractions',
            name='tags',
        ),
    ]
