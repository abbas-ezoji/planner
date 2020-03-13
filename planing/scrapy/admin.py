from django.contrib import admin
from .models import points
from .apps import scrapy
from sqlalchemy import create_engine
from django.conf import settings
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError

db_connection_url = "postgresql://{}:{}@{}:{}/{}".format(
    settings.DATABASES['default']['USER'],
    settings.DATABASES['default']['PASSWORD'],
    settings.DATABASES['default']['HOST'],
    settings.DATABASES['default']['PORT'],
    settings.DATABASES['default']['NAME'],
)

engine = create_engine(db_connection_url)


def update_points():
    s = scrapy()
    data = s.get_data()

    df = pd.DataFrame(list(points.objects.all().values()),
                      columns=['type', 'title', 'location', 'details', 'image'])
    last_data = df['details']
    data = data[~data.details.isin(last_data)]
    print('titles: ' + data)
    try:
        data.to_sql(points._meta.db_table, engine, if_exists='append', index=False, chunksize=10000)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)


class PointsAdmin(admin.ModelAdmin):
    # update_points()
    list_display = ('type', 'title', 'location', 'details', 'image',)
    list_filter = ('type', 'title', 'location',)


admin.site.register(points, PointsAdmin)
