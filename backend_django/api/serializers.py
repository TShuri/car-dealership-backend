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

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id_client', 'name', 'phone', 'passport', 'email']

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id_employee', 'name', 'post', 'salary', 'email']

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id_service', 'date', 'status', 'id_car']