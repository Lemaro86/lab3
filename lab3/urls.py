"""
URL configuration for lab3 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from stocks import views
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path(r'service/', views.ServiceList.as_view(), name='service-list'),
    path(r'service/<int:pk>/', views.ServiceDetail.as_view(), name='service-detail'),
    path(r'service/<int:pk>/put/', views.put_detail_service, name='service-put'),
    path(r'order/', views.OrderList.as_view(), name='order-list'),
    path(r'order/<int:pk>/', views.OrderDetail.as_view(), name='order-detail'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path(r'users/', views.UsersList.as_view(), name='users-list'),
]
