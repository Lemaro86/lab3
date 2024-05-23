import datetime

from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BaseAuthentication
from django.shortcuts import get_object_or_404
from rest_framework import status

from stocks.permissions import IsAdmin, IsManager, IsUser
from stocks.serializers import UserSerializer, ServiceSerializer, OrderSerializer, UserRoleSerializer
from stocks.minio import add_pic
from stocks.models import Service
from stocks.models import Order
from stocks.models import CustomUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
import redis
import uuid
from django.utils import timezone
from django.db import models

session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


def method_permission_classes(classes):
    def decorator(func):
        def decorated_func(self, *args, **kwargs):
            self.permission_classes = classes
            self.check_permissions(self.request)
            return func(self, *args, **kwargs)

        return decorated_func

    return decorator


@permission_classes([AllowAny])
@authentication_classes([])
@csrf_exempt
@swagger_auto_schema(method='post', request_body=UserSerializer)
@api_view(['Post'])
def login_view(request):
    email = request.data["email"]
    password = request.data["password"]
    user = authenticate(request, email=email, password=password)
    if user is not None:
        random_key = str(uuid.uuid4())
        session_storage.set(random_key, email)

        login(request, user)
        user_item = CustomUser.objects.get(email=email)
        serializer = UserRoleSerializer(user_item)
        response = Response(serializer.data)
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = 'Access-Control-Allow-Headers, Origin, Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers, credentials'
        response.set_cookie("session_id", random_key)

        return response
    else:
        return HttpResponse("{'status': 'error', 'error': 'login failed'}")


@swagger_auto_schema(method='get')
@api_view(['Get'])
@permission_classes([AllowAny])
@authentication_classes([])
def logout_view(request):
    logout(request._request)
    response = Response({'status': 'Success'})
    response.delete_cookie('session_id')
    response.delete_cookie('sessionid')
    response.delete_cookie('X-CSRF-Token')
    return response


@permission_classes([AllowAny])
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    model_class = CustomUser

    def create(self, request):
        if self.model_class.objects.filter(email=request.data['email']).exists():
            return Response({'status': 'Exist'}, status=400)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            self.model_class.objects.create_user(email=serializer.data['email'],
                                                 password=serializer.data['password'],
                                                 is_superuser=serializer.data['is_superuser'],
                                                 is_staff=serializer.data['is_staff'])
            return Response({'status': 'Success'}, status=200)
        return Response({'status': 'Error', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [AllowAny]
        elif self.action in ['list']:
            permission_classes = [IsAdmin, IsManager]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]


class ServiceList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    model_class = Service
    serializer_class = ServiceSerializer

    get_response = openapi.Response('Get service list', serializer_class(many=True))

    @swagger_auto_schema(responses={200: get_response})
    def get(self, request, format=None):
        title = request.GET.get('title')
        if title and title != '':
            service = self.model_class.objects.filter(title__contains=title)
        else:
            service = self.model_class.objects.all()
        serializer = self.serializer_class(service, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ServiceSerializer, responses={200: ServiceSerializer})
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            service = serializer.save()
            service.save()
            pic = request.FILES.get("pic")
            pic_result = add_pic(service, pic)
            if 'error' in pic_result.data:
                return pic_result
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    model_class = Service
    serializer_class = ServiceSerializer

    def get(self, request, pk, format=None):
        service = get_object_or_404(self.model_class, pk=pk)
        serializer = self.serializer_class(service)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ServiceSerializer)
    @method_permission_classes((IsAdmin,))
    @authentication_classes([SessionAuthentication, BaseAuthentication])
    def put(self, request, pk, format=None):
        if 'session_id' in request.COOKIES.keys():
            ssid = request.COOKIES["session_id"]
            session = session_storage.get(ssid)
            session_str = session.decode('utf-8')
            user_info = CustomUser.objects.filter(email__contains=session_str)
            if user_info.exists() and user_info[0].is_superuser:
                service = get_object_or_404(self.model_class, pk=pk)
                serializer = self.serializer_class(service, data=request.data, partial=True)
                if 'pic' in serializer.initial_data:
                    pic_result = add_pic(service, serializer.initial_data['pic'])
                    if 'error' in pic_result.data:
                        return pic_result
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return HttpResponse("{'status': '401', 'error': 'cookies is not found'}")
        else:
            return HttpResponse("{'status': '401', 'error': 'cookies is not found'}")

    @method_permission_classes((IsAdmin,))
    def delete(self, request, pk, format=None):
        service = get_object_or_404(self.model_class, pk=pk)
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def cookie_to_email(self, request):
    if 'session_id' in request.COOKIES.keys():
        ssid = request.COOKIES["session_id"]
        session = session_storage.get(ssid)
        session_str = session.decode('utf-8')
        user = CustomUser.objects.filter(email__contains=session_str)
        if user.exists():
            return user[0]
        else:
            return HttpResponse("{'status': '401', 'error': 'cookies is not found'}")
    else:
        return HttpResponse("{'status': '401', 'error': 'cookies is not found'}")


class OrderList(APIView):
    permission_classes = [IsAuthenticated]
    model_class = Order
    serializer_class = OrderSerializer
    get_response = openapi.Response('Get order list', serializer_class(many=True))

    @swagger_auto_schema(responses={200: get_response})
    @method_permission_classes([IsUser, ])
    @authentication_classes([SessionAuthentication, BaseAuthentication])
    def get(self, request, format=None):
        user = cookie_to_email(self, request)
        if user and (user.is_staff or user.is_superuser):
            order = self.model_class.objects.all()
        else:
            order = self.model_class.objects.filter(creator_id=user.pk)
        serializer = self.serializer_class(order, many=True)
        return Response(serializer.data)

    @method_permission_classes([IsUser, ])
    @authentication_classes([SessionAuthentication, BaseAuthentication])
    def post(self, request, format=None):
        user = cookie_to_email(self, request)
        creator_id = user.pk
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            order = serializer.save(creator_id=creator_id)
            order.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetail(APIView):
    # permission_classes = [IsAuthenticated]
    model_class = Order
    serializer_class = OrderSerializer
    get_response = openapi.Response('Get order by id', serializer_class())

    @swagger_auto_schema(responses={200: get_response})
    @method_permission_classes([IsAdmin, IsManager, ])
    @authentication_classes([SessionAuthentication, BaseAuthentication])
    def get(self, request, pk, format=None):
        order = get_object_or_404(self.model_class, pk=pk)
        serializer = self.serializer_class(order)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=OrderSerializer, responses={200: get_response})
    @method_permission_classes([IsAdmin, IsManager, ])
    @authentication_classes([SessionAuthentication, BaseAuthentication])
    def put(self, request, pk, format=None):
        user = cookie_to_email(self, request)
        moderator_id = user.pk
        order = get_object_or_404(self.model_class, pk=pk)
        serializer = self.serializer_class(order, data=request.data, partial=True)
        if serializer.is_valid():
            tz = timezone.get_current_timezone()
            start = datetime.datetime.now().replace(tzinfo=tz)
            if request.data["status"] == "activated":
                serializer.save(moderator_id=moderator_id, activated=start)
            elif request.data["status"] == "completed" or request.data["status"] == "declined":
                serializer.save(completed=start)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_permission_classes([IsAdmin, IsManager, ])
    @authentication_classes([SessionAuthentication, BaseAuthentication])
    def delete(self, request, pk, format=None):
        order = get_object_or_404(self.model_class, pk=pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
