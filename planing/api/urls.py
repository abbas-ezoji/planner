from django.urls import path
from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^filter/', include('api.filter.urls')),
    # url(r'^users/', include('api.users.urls')),
    path('country/', views.ListCountry.as_view()),
    path('country/<int:pk>/', views.ListCountry.as_view()),
    path('province/', views.ListProvince.as_view()),
    path('province/<int:pk>/', views.ListProvince.as_view()),
    path('city/', views.ListCity.as_view()),
    path('city/<int:pk>/', views.ListCity.as_view()),
    path('attraction/', views.ListAttraction.as_view()),
    path('attraction/<int:pk>/', views.ListAttraction.as_view()),
    path('plan_details/', views.ListPlan_details.as_view()),
    path('plan_details/<int:pk>/', views.ListPlan_details.as_view()),

]