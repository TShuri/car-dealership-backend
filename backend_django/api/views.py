from django.shortcuts import render
from rest_framework.views import APIView
from .models import Car, Deal
from .serializers import CarSerializer, DealSerializer
from rest_framework.response import Response
from django.db.models import F

# Create your views here.
class CarsView(APIView):
    def get(self, request):
        query = Car.objects\
            .values('id_car', 'brand', 'model', 'color', 'price', 'engine', 'power', 'gearbox') \
            .exclude(id_car__in=Deal.objects.values('id_car'))

        # print(len(query))
        print(request.GET.get('page'))
        if (request.GET.get('id')):
            print('id have')

        end = int(request.GET.get('page')) * 20
        start = int(end - 20)
        print(start, '-', end)
        return Response(query[start:end], headers={'X-Total-Count': len(query)})

    def post(self, request):
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)