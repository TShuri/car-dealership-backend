from django.shortcuts import render
from rest_framework.views import APIView
from .models import Car, Deal, Client, Employee, Service
from .serializers import CarSerializer, DealSerializer, ClientSerializer, EmployeeSerializer, ServiceSerializer
from rest_framework.response import Response
from django.db.models import F

# Create your views here.
class CarsView(APIView):
    def get(self, request):
        query = Car.objects\
            .values('id_car', 'brand', 'model', 'color', 'price', 'engine', 'power', 'gearbox') \
            .exclude(id_car__in=Deal.objects.values('id_car'))

        if request.GET.get('brand'):
            query = query.filter(brand=request.GET.get('brand'))
        if request.GET.get('model'):
            query = query.filter(model__icontains=request.GET.get('model'))
        if request.GET.get('year'):
            query = query.filter(model__icontains=request.GET.get('year'))
        if request.GET.get('color'):
            query = query.filter(color=request.GET.get('color'))
        if request.GET.get('engine'):
            query = query.filter(engine=request.GET.get('engine'))
        if request.GET.get('gearbox'):
            query = query.filter(gearbox=request.GET.get('gearbox'))
        if request.GET.get('powerFrom'):
            query = query.filter(power__gte=request.GET.get('powerFrom'))
        if request.GET.get('powerTo'):
            query = query.filter(power__lte=request.GET.get('powerTo'))
        if request.GET.get('priceFrom'):
            query = query.filter(price__gte=request.GET.get('priceFrom'))
        if request.GET.get('priceTo'):
            query = query.filter(price__lte=request.GET.get('priceTo'))

        print('page: ', request.GET.get('page'))
        print('countsCar: ', len(query))

        end = int(request.GET.get('page')) * 20
        start = int(end - 20)

        data = Response(query[start:end])
        data['Count'] = len(query)

        if (end > len(query)) and (request.GET.get('page') != '1'):
            return Response({'Empty':True})
        else:
            return data

    def post(self, request):
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

class DealsView(APIView):
    def get(self, request):
        query = Deal.objects \
            .select_related('id_car')\
            .values() \
            .filter(id_client=request.GET.get('id_client'))

        return Response(query)