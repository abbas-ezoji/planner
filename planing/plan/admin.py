from django.contrib import admin
from .models import (attractions, travelType, distance_mat,
                     country, province, city)


class attractionsAdmin(admin.ModelAdmin):
    # pass
    list_display = ('title', 'country', 'province', 'city',
                    'latt', 'long', 'rq_time', 'vis_time',)
    list_filter = ('country', 'province', 'city', 'title',)


class travelTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'tags',)
    list_filter = ('title', 'tags',)


class distance_matAdmin(admin.ModelAdmin):
    # pass
    list_display = [field.name for field in distance_mat._meta.get_fields()]
    list_filter = ('origin__country', 'origin__province', 'origin__city', 'origin__title',
                   'destination__title','travel_type__title')


class countryAdmin(admin.ModelAdmin):
    list_display = ('name', 'iso3', 'phoneCode',)
    list_filter = ('name', 'iso3', 'phoneCode',)


class provinceAdmin(admin.ModelAdmin):
    list_display = ('name',  'phoneCode', )
    list_filter = ('name',  'phoneCode', 'country__name',)


class cityAdmin(admin.ModelAdmin):
    # pass
    list_display = ('name',  'phoneCode', 'latt', 'long')
    list_filter = ('name',  'phoneCode', 'province__name', 'province__country__name')


admin.site.register(country, countryAdmin)
admin.site.register(province, provinceAdmin)
admin.site.register(city, cityAdmin)
admin.site.register(attractions, attractionsAdmin)
admin.site.register(travelType, travelTypeAdmin)
admin.site.register(distance_mat, distance_matAdmin)
