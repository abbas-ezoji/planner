from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from django_filters import rest_framework as filters
from django.db.models import Sum, Count
from plan import models
from api import serializers
import datetime


# class attractionFilter(filters.FilterSet):
#     rq_time__lt = filters.DateFilter(field_name='rq_time', lookup_expr='lt', distinct=True)
#     rq_time__gt = filters.DateFilter(field_name='rq_time', lookup_expr='gt', distinct=True)
#     type = filters.NumberFilter(field_name='type', method='sum_ststus')
#     villaCategory = filters.NumberFilter(field_name='villaCategory', distinct=True)
#
#     class Meta:
#         model = models.attraction
#         fields = ('villaCategory', 'date__lt', 'date__gt', 'status')


@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny, ])
def planView(request):
    # permission_classes = (IsAuthenticated,)
    plan_id = request.GET.get('id', 0)
    city = request.GET.get('city', 0)
    days = request.GET.get('days', 0)

    query = 'SELECT * FROM [dbo].[plan_GetPlans] ({},{},{})'.format(plan_id, city, days)
    # print(query)
    plan = models.plan.objects.raw(query)
    serializer = serializers.SerializerPlan(plan, many=True)

    return Response(serializer.data)