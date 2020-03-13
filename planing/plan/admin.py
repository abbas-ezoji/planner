from django.contrib import admin
from .models import attractions, travelType, distance_mat


class attractionsAdmin(admin.ModelAdmin):
    list_display = ('country', 'iso3', 'province', 'city', 'fullTitle', 'description',
                    'latt', 'long', 'rq_time', 'vis_time',)
    list_filter = ('country', 'province', 'city', 'title',)


class travelTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'tags',)
    list_filter = ('title', 'tags',)


class distance_matAdmin(admin.ModelAdmin):
    list_display = [field.name for field in distance_mat._meta.get_fields()]
    list_filter = ('origin__country', 'origin__province', 'origin__city', 'origin__title',
                   'destination__title',)


admin.site.register(attractions, attractionsAdmin)
admin.site.register(travelType, travelTypeAdmin)
admin.site.register(distance_mat, distance_matAdmin)
