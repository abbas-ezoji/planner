# Generated by Django 2.1.15 on 2020-04-12 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
            ],
            options={
                'verbose_name_plural': '3 Airports',
                'ordering': ('city', 'airport_en'),
            },
        ),
        migrations.CreateModel(
            name='attractions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(0, 'Attraction'), (1, 'Fooding'), (2, 'Resting'), (3, 'Healthing'), (4, 'Others')], default=0, verbose_name='Selection Type')),
                ('phoneCode', models.CharField(blank=True, max_length=10, null=True, verbose_name='Phone Code')),
                ('title', models.CharField(blank=True, max_length=200, null=True, verbose_name='Title')),
                ('fullTitle', models.TextField(blank=True, null=True, verbose_name='Full Title')),
                ('address', models.CharField(blank=True, max_length=2000, null=True, verbose_name='Address')),
                ('cost', models.CharField(blank=True, max_length=50, null=True, verbose_name='Cost')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('latt', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Latitude')),
                ('long', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Longitude')),
                ('rq_time', models.IntegerField(blank=True, null=True, verbose_name='Require Time')),
                ('vis_time', models.CharField(blank=True, max_length=50, null=True, verbose_name='Visit Time Range')),
                ('vis_time_from', models.IntegerField(blank=True, null=True, verbose_name='Visit Time From')),
                ('vis_time_to', models.IntegerField(blank=True, null=True, verbose_name='Visit Time To')),
                ('like_no', models.IntegerField(blank=True, null=True, verbose_name='Likes')),
                ('view_no', models.IntegerField(blank=True, null=True, verbose_name='Views')),
                ('image', models.URLField(blank=True, null=True, verbose_name='Image')),
            ],
            options={
                'verbose_name_plural': '4 Attractions',
                'ordering': ('latt', 'long'),
            },
        ),
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50, null=True, verbose_name='Title')),
                ('comments', models.TextField(blank=True, null=True, verbose_name='Comments')),
            ],
        ),
        migrations.CreateModel(
            name='city',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='City Name')),
                ('phoneCode', models.CharField(blank=True, max_length=10, null=True, verbose_name='Phone Code')),
                ('latt', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Latitude')),
                ('long', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Longitude')),
            ],
            options={
                'verbose_name_plural': '2 City',
            },
        ),
        migrations.CreateModel(
            name='constraint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True, verbose_name='Title')),
                ('type', models.IntegerField(choices=[(0, 'Attraction'), (1, 'Fooding'), (2, 'Resting'), (3, 'Healthing'), (4, 'Others')], default=1, verbose_name='Selection Type')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('rq_time', models.IntegerField(blank=True, null=True, verbose_name='Require Time')),
                ('vis_time_from', models.IntegerField(blank=True, null=True, verbose_name='Visit Time From')),
                ('vis_time_to', models.IntegerField(blank=True, null=True, verbose_name='Visit Time To')),
            ],
            options={
                'verbose_name_plural': '4 Constraints',
            },
        ),
        migrations.CreateModel(
            name='country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Country Name')),
                ('iso3', models.CharField(blank=True, max_length=10, null=True, verbose_name='IOS3')),
                ('phoneCode', models.CharField(blank=True, max_length=10, null=True, verbose_name='Phone Code')),
            ],
            options={
                'verbose_name_plural': '0 Country',
            },
        ),
        migrations.CreateModel(
            name='department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50, null=True, verbose_name='Title')),
                ('comments', models.TextField(blank=True, null=True, verbose_name='Comments')),
            ],
        ),
        migrations.CreateModel(
            name='distance_mat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ecl_dist', models.FloatField(blank=True, null=True, verbose_name='Euclidean Distance')),
                ('len_meter', models.FloatField(blank=True, null=True, verbose_name='Lenght Of Meters')),
                ('len_time', models.FloatField(blank=True, null=True, verbose_name='Lenght Of Time')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination', to='plan.attractions')),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='distance_mat', to='plan.attractions')),
            ],
            options={
                'verbose_name_plural': '6 Distance matrix',
            },
        ),
        migrations.CreateModel(
            name='plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('present_id', models.CharField(blank=True, max_length=1000, null=True)),
                ('day', models.IntegerField(blank=True, null=True, verbose_name='Day Of Tour')),
                ('coh_fullTime', models.FloatField(blank=True, null=True, verbose_name='Coefficient of Fill full time Cost')),
                ('coh_lengthTime', models.FloatField(blank=True, null=True, verbose_name='Coefficient of distance length time Cost')),
                ('coh_countPoints', models.FloatField(blank=True, null=True, verbose_name='Coefficient of count of points Cost')),
                ('coh_minRqTime', models.FloatField(blank=True, null=True, verbose_name='Coefficient of diff min required Time Cost')),
                ('cost_fullTime', models.FloatField(blank=True, null=True, verbose_name='Fill full time Cost')),
                ('cost_lengthTime', models.FloatField(blank=True, null=True, verbose_name='Distance length time Cost')),
                ('cost_countPoints', models.FloatField(blank=True, null=True, verbose_name='Count of points Cost')),
                ('cost_minRqTime', models.FloatField(blank=True, null=True, verbose_name='Diff min required Time Cost')),
                ('start_time', models.CharField(blank=True, max_length=20, null=True, verbose_name='Start Time of Day')),
                ('end_time', models.CharField(blank=True, max_length=20, null=True, verbose_name='End Time of Day')),
                ('dist_len', models.FloatField(blank=True, null=True, verbose_name='Length of distance times')),
                ('points_len', models.IntegerField(blank=True, null=True, verbose_name='Count of points used')),
                ('duration_len', models.FloatField(blank=True, null=True, verbose_name='Length of duration points')),
                ('tags', models.CharField(blank=True, max_length=1000, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.city')),
            ],
            options={
                'verbose_name_plural': '7 Plan',
            },
        ),
        migrations.CreateModel(
            name='plan_details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('len_time', models.IntegerField()),
                ('from_time', models.IntegerField(blank=True, null=True)),
                ('dist_to', models.IntegerField(blank=True, null=True)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.plan')),
                ('point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.attractions')),
            ],
            options={
                'verbose_name_plural': '7.1 Plan details',
                'ordering': ('plan__day', 'order'),
            },
        ),
        migrations.CreateModel(
            name='province',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Province Name')),
                ('phoneCode', models.CharField(blank=True, max_length=10, null=True, verbose_name='Phone Code')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='plan.country')),
            ],
            options={
                'verbose_name_plural': '1 Province',
            },
        ),
        migrations.CreateModel(
            name='tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50, null=True, verbose_name='Tag Title')),
                ('comments', models.TextField(blank=True, null=True, verbose_name='Comments')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='plan.category')),
            ],
        ),
        migrations.CreateModel(
            name='travelType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('tags', models.CharField(max_length=1000)),
                ('comment', models.TextField()),
            ],
            options={
                'verbose_name_plural': '5 Travel Types',
            },
        ),
        migrations.AddField(
            model_name='distance_mat',
            name='travel_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.travelType'),
        ),
        migrations.AddField(
            model_name='constraint',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='plan.tags'),
        ),
        migrations.AddField(
            model_name='city',
            name='province',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='plan.province'),
        ),
        migrations.AddField(
            model_name='category',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='plan.department'),
        ),
        migrations.AddField(
            model_name='attractions',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='plan.city'),
        ),
        migrations.AddField(
            model_name='attractions',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='plan.country'),
        ),
        migrations.AddField(
            model_name='attractions',
            name='province',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='plan.province'),
        ),
        migrations.AddField(
            model_name='attractions',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='plan.tags'),
        ),
        migrations.AddField(
            model_name='airport',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='plan.city'),
        ),
    ]
