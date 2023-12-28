from django.shortcuts import render
from rest_framework.views import APIView, status
from .models import Car, Deal, Client, Employee, Service, User
from .serializers import (CarSerializer, DealSerializer, ClientSerializer, EmployeeSerializer,
                          ServiceSerializer, UserSerializer)
from rest_framework.response import Response
import datetime
from django.db.models import F, Count
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404

# Create your views here.
class AuthView(APIView):
    def post(self, request):
        email = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            #serialized_user = UserSerializer(user)
            group = user.groups.get()

            print(user)
            print(group)

            if str(group) == "Client":
                query = (Client.objects.values('id_client', 'name').filter(email=user))[0]
                id = query['id_client']
                name = query['name']
                print(id, name)

                return Response({
                    'id': str(id),
                    'login': str(user),
                    'group': str(group),
                    'name': str(name)
                })

            if str(group) == "Employee":
                query = (Employee.objects.values('id_employee', 'name').filter(email=user))[0]
                id = query['id_employee']
                name = query['name']
                print(id, name)

                return Response({
                    'id': str(id),
                    'login': str(user),
                    'group': str(group),
                    'name': str(name)
                })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

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

class DealsClientView(APIView):
    def get(self, request):
        query = Deal.objects \
            .select_related('id_car', 'id_employee', 'id_client') \
            .values('id_deal', 'date',
                    'id_car_id', 'id_car__brand', 'id_car__model', 'id_car__price',
                    'id_employee__post', 'id_employee__name', 'id_employee__email',
                    'id_client__name', 'id_client__email', 'id_client__phone')
        query = query.filter(id_client=request.GET.get('id_client'))

        # print(len(query))
        # print(request.GET.get('id_client'))
        return Response(query)

class DealsEmployeeView(APIView):
    def get(self, request):
        query = Deal.objects \
            .select_related('id_car', 'id_employee', 'id_client') \
            .values('id_deal', 'date',
                    'id_car_id', 'id_car__brand', 'id_car__model', 'id_car__price',
                    'id_employee__post', 'id_employee__name', 'id_employee__email',
                    'id_client__name', 'id_client__email', 'id_client__phone')
        query = query.filter(id_employee=request.GET.get('id_employee'))

        if request.GET.get('brand'):
            query = query.filter(id_car__brand=request.GET.get('brand'))
        if request.GET.get('model'):
            query = query.filter(id_car__model__icontains=request.GET.get('model'))

        print('page: ', request.GET.get('page'))
        print('countsCar: ', len(query))

        end = int(request.GET.get('page')) * 20
        start = int(end - 20)

        data = Response(query[start:end])

        if (end > len(query)) and (request.GET.get('page') != '1'):
            return Response({'Empty': True})
        else:
            return data

class ServicesClientView(APIView):
    def get(self, request):
        query = Deal.objects \
            .select_related('id_car')\
            .values('id_car', 'id_car__brand', 'id_car__model', 'id_car__color')\
            .filter(id_client=request.GET.get('id_client'))

        print(len(query))

        return Response(query)

class ServicesEmployeeView(APIView):
    def get(self, request):
        query = Deal.objects \
            .select_related('id_car', 'id_client') \
            .values('id_car', 'id_car__brand', 'id_car__model', 'id_car__color',
                    'id_client__name')
        query = query.filter(id_employee=request.GET.get('id_employee'))

        if request.GET.get('brand'):
            query = query.filter(id_car__brand=request.GET.get('brand'))
        if request.GET.get('model'):
            query = query.filter(id_car__model__icontains=request.GET.get('model'))

        print('page: ', request.GET.get('page'))
        print('countsCar: ', len(query))

        end = int(request.GET.get('page')) * 20
        start = int(end - 20)

        data = Response(query[start:end])

        if (end > len(query)) and (request.GET.get('page') != '1'):
            return Response({'Empty': True})
        else:
            return data

class ServicesHistoryView(APIView):
    def get(self, request):
        query = Service.objects \
            .values('id_car', 'id_service', 'date', 'status') \
            .filter(id_car=request.GET.get('id_car'))

        return Response(query)

    def post(self, request):
        query = Service.objects \
            .values('date') \
            .filter(id_car=request.data['id_car']) \
            .order_by('-date')
        latest_service = query.first()

        received_date = datetime.datetime.strptime(request.data['date'], "%Y-%m-%d").date()
        latest_date = datetime.datetime.strptime(str(latest_service['date']), "%Y-%m-%d").date()

        if received_date > latest_date:
            print("received_date больше, чем latest_date")
            serializer = ServiceSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response('ok')
        else:
            print("received_date меньше или равна latest_date")
            return Response(str(latest_date))