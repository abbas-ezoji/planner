from django.contrib.auth.models import User, Group
from rest_framework import serializers
from plan import models


class SerializerCountry(serializers.ModelSerializer):
    class Meta:
        model = models.country
        fields = '__all__'


class SerializerProvince(serializers.ModelSerializer):
    class Meta:
        model = models.province
        fields = '__all__'


class SerializerCity(serializers.ModelSerializer):
    class Meta:
        model = models.city
        fields = '__all__'


class SerializerAttraction(serializers.ModelSerializer):
    class Meta:
        model = models.attraction
        fields = '__all__'
