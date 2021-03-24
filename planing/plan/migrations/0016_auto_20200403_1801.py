# Generated by Django 2.1.15 on 2020-04-03 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0015_attractions_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='constraint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True, verbose_name='Title')),
                ('type', models.IntegerField(choices=[(1, 'Fooding'), (2, 'Resting'), (3, 'Healthing'), (4, 'Others')], default=1, verbose_name='Selection Type')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('rq_time', models.IntegerField(blank=True, null=True, verbose_name='Require Time')),
                ('vis_time_from', models.IntegerField(blank=True, null=True, verbose_name='Visit Time From')),
                ('vis_time_to', models.IntegerField(blank=True, null=True, verbose_name='Visit Time To')),
                ('tags', models.ManyToManyField(blank=True, null=True, to='plan.tags')),
            ],
            options={
                'verbose_name_plural': '4 Constraints',
            },
        ),
        migrations.RemoveField(
            model_name='attractions',
            name='type',
        ),
        migrations.AlterField(
            model_name='attractions',
            name='address',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='attractions',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Title'),
        ),
    ]