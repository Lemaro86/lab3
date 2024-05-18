from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from stocks.serializers import  UserSerializer, ServiceSerializer, OrderSerializer
from stocks.models import AuthUser
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from stocks.minio import add_pic
from stocks.models import Service
from stocks.models import Order


def user():
    try:
        user1 = AuthUser.objects.get(id=1)
    except:
        user1 = AuthUser(id=1, first_name="Иван", last_name="Иванов", password=1234, username="user1")
        user1.save()
    return user1


class UsersList(APIView):
    model_class = AuthUser
    serializer_class = UserSerializer

    def get(self, request, format=None):
        user = self.model_class.objects.all()
        serializer = self.serializer_class(user, many=True)
        return Response(serializer.data)


class ServiceList(APIView):
    model_class = Service
    serializer_class = ServiceSerializer

    def get(self, request, format=None):
        title = request.GET.get('title')
        if title and title != '':
            service = self.model_class.objects.filter(title__contains=title)
        else:
            service = self.model_class.objects.all()
        serializer = self.serializer_class(service, many=True)
        return Response(serializer.data)

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
    model_class = Service
    serializer_class = ServiceSerializer

    def get(self, request, pk, format=None):
        service = get_object_or_404(self.model_class, pk=pk)
        serializer = self.serializer_class(service)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
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

    def delete(self, request, pk, format=None):
        service = get_object_or_404(self.model_class, pk=pk)
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['Put'])
def put_detail_service(self, request, pk, format=None):
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


class OrderList(APIView):
    model_class = Order
    serializer_class = OrderSerializer

    def get(self, request, format=None):
        order = self.model_class.objects.all()
        serializer = self.serializer_class(order, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            order.save()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetail(APIView):
    model_class = Order
    serializer_class = OrderSerializer

    def get(self, request, pk, format=None):
        order = get_object_or_404(self.model_class, pk=pk)
        serializer = self.serializer_class(order)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        order = get_object_or_404(self.model_class, pk=pk)
        serializer = self.serializer_class(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        order = get_object_or_404(self.model_class, pk=pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
