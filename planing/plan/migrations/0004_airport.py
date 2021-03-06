# Generated by Django 2.1.15 on 2020-03-19 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0003_auto_20200318_1633'),
    ]

    operations = [
        migrations.CreateModel(
            name='airport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Name')),
                ('icao', models.CharField(blank=True, max_length=10, null=True, verbose_name='ICAO')),
                ('iata', models.CharField(blank=True, max_length=10, null=True, verbose_name='IATA')),
                ('type', models.CharField(blank=True, max_length=20, null=True, verbose_name='Type')),
                ('url', models.CharField(blank=True, max_length=100, null=True, verbose_name='Address url')),
                ('area_code', models.CharField(blank=True, max_length=100, null=True, verbose_name='Area code')),
                ('country_code', models.CharField(blank=True, max_length=100, null=True, verbose_name='Country code')),
                ('city_en', models.CharField(blank=True, max_length=100, null=True, verbose_name='City En')),
                ('airport_en', models.CharField(blank=True, max_length=100, null=True, verbose_name='AirPort name')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='plan.city')),
            ],
            options={
                'verbose_name_plural': '7.1 Plan details',
                'ordering': ('city', 'airport_en'),
            },
        ),
    ]
