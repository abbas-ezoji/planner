from django.contrib import admin
from .models import (attraction, travelType, distance_mat,
                     country, province, city, plan, plan_details,
                     airport, constraint)


class attractionAdmin(admin.ModelAdmin):
    # pass
    list_display = ('title' , 'country', 'province', 'city',
                    'latt', 'long', 'rq_time', 'vis_time',)
    list_filter = ('country', 'province', 'city', 'tags__title', 'title', 'type',)


class constraintAdmin(admin.ModelAdmin):
    # pass
    list_display = ('title', 'type', 'rq_time', 'vis_time_from', 'vis_time_to')
    list_filter = ('title', 'type', 'tags__title', 'rq_time', 'vis_time_from', 'vis_time_to')


class travelTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'tags',)
    list_filter = ('title', 'tags',)


class distance_matAdmin(admin.ModelAdmin):
    # pass
    list_display = [field.name for field in distance_mat._meta.get_fields()]
    list_filter = ('origin__country', 'origin__province', 'origin__city', 'origin__title',
                   'destination__title', 'travel_type__title')


class countryAdmin(admin.ModelAdmin):
    list_display = ('name', 'iso3', 'phoneCode',)
    list_filter = ('name', 'iso3', 'phoneCode',)


class provinceAdmin(admin.ModelAdmin):
    list_display = ('name', 'phoneCode',)
    list_filter = ('name', 'phoneCode', 'country__name',)


class cityAdmin(admin.ModelAdmin):
    # pass
    list_display = ('name', 'phoneCode', 'latt', 'long')
    list_filter = ('name', 'phoneCode', 'province__name', 'province__country__name')


class planAdmin(admin.ModelAdmin):
    # pass
    list_display = ('city', 'present_id','cost_fullTime', 'cost_lengthTime', 'cost_countPoints', 'cost_minRqTime','cost_rate', 'tags')
    list_filter = ('city__name', 'tags', 'all_days','cost_lengthTime', 'cost_countPoints', 'cost_minRqTime',)


class plan_detailsAdmin(admin.ModelAdmin):
    pass
    list_display = ('point', 'order', 'from_time', 'len_time', 'dist_to', 'plan',)
    list_filter = ('plan__city__name', 'point__title', 'plan__present_id',
                   'plan__cost_fullTime', 'plan__cost_lengthTime', 'plan__cost_countPoints', 'plan__cost_minRqTime',
                   'plan__cost_rate')


class airportAdmin(admin.ModelAdmin):
    # pass
    list_display = ('name', 'city', 'iata', 'type', 'airport_en')
    list_filter = ('city__province__country__name', 'city__province__name', 'city__name',
                   'airport_en',)


admin.site.register(airport, airportAdmin)
admin.site.register(constraint, constraintAdmin)
admin.site.register(plan, planAdmin)
admin.site.register(plan_details, plan_detailsAdmin)
admin.site.register(country, countryAdmin)
admin.site.register(province, provinceAdmin)
admin.site.register(city, cityAdmin)
admin.site.register(attraction, attractionAdmin)
admin.site.register(travelType, travelTypeAdmin)
admin.site.register(distance_mat, distance_matAdmin)
