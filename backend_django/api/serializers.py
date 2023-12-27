from rest_framework import serializers
from .models import Car, Client, Deal, Employee, Service

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id_car', 'brand', 'model', 'color', 'price', 'engine', 'power', 'gearbox']

class DealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = ['id_deal', 'id_car', 'id_client', 'id_employee', 'date']