from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_list_or_404, get_object_or_404
from plan import models
from . import serializers
import datetime


@permission_classes([AllowAny, ])
class ListCountry(generics.ListCreateAPIView):
    queryset = models.country.objects.all()
    serializer_class = serializers.SerializerCountry

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.multiple_lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


@permission_classes([AllowAny, ])
class ListProvince(generics.ListCreateAPIView):
    queryset = models.province.objects.all()
    serializer_class = serializers.SerializerProvince


@permission_classes([AllowAny, ])
class ListCity(generics.ListCreateAPIView):
    queryset = models.city.objects.all()
    serializer_class = serializers.SerializerCity


@permission_classes([AllowAny, ])
class ListAttraction(generics.ListCreateAPIView):
    queryset = models.attraction.objects.all()
    serializer_class = serializers.SerializerAttraction


@permission_classes([AllowAny, ])
class ListPlan_details(generics.ListCreateAPIView):
    queryset = models.plan_details.objects.all()
    serializer_class = serializers.SerializerPlan_details

# @permission_classes([AllowAny, ])
# def getTourPics(request, tour_id):
#     # Delegate to the view generic and get an HttpResponse.
#     response = ListTodoPictures.get_object(
#         request,
#         queryset=models.Pictures.objects.filter(id=tour_id),
#         object_id=tour_id,
#     )
#
#     # Record the last accessed date. We do this *after* the call
#     # to object_detail(), not before it, so that this won't be called
#     # unless the Author actually exists. (If the author doesn't exist,
#     # object_detail() will raise Http404, and we won't reach this point.)
#     now = datetime.datetime.now()
#     models.Pictures.objects.filter(id=tour_id).update(last_accessed=now)
#     return response
