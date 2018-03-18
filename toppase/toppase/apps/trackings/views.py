# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView

from .serializers import StoreSerialiser, OrderSerializer, OrderCSVSerialiser, ProductSerialiser, CourierSerialiser
from .tasks import create_orders_from_order_csv
from .models import Order, Product
from ..accounts.models import Store, Courier
from .permissions import OrderApiPermissions, StoreApiPermissions, CourierApiPermissions

import logging


class TrackingBusinessView(TemplateView):
    """ Tracking related to business """
    template_name = "trackings/tracking.html"


class TrackingDashboradView(TemplateView):
    """ Tracking Performance In last 28 days """
    template_name = "trackings/dashboard.html"


class OrderDetailView(TemplateView):
    """ Order Details and update """
    template_name = "trackings/order_detail.html"

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['order_history'] = get_object_or_404(Order, id=self.kwargs['pk']).events_history
        return context


# API VIEWSETS

class StoreViewSet(viewsets.ModelViewSet):
    # queryset = Store.objects.all()
    serializer_class = StoreSerialiser
    permission_classes = (permissions.IsAuthenticated, StoreApiPermissions)

    def get_queryset(self, **kwargs):
        return Store.objects.filter(id=self.request.user.get_store().id)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerialiser
    permission_classes = (permissions.IsAuthenticated,)



class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated, OrderApiPermissions)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class OrderCSVCreateApiView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCSVSerialiser
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            return Response({"Fail": "Please enter a non empty valid csv file"}, status=status.HTTP_400_BAD_REQUEST)
        upload_obj = serializer.save()
        # Lunch celery task
        create_orders_from_order_csv.delay(str(upload_obj.file_csv), request.user.email, request.user.get_store().id,
                                           upload_obj.id)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CourierViewSet(viewsets.ModelViewSet):
    serializer_class = CourierSerialiser
    permission_classes = (permissions.IsAuthenticated, CourierApiPermissions)

    def get_queryset(self, **kwargs):
        return Courier.objects.filter(code__in=self.request.user.get_store().get_couriers())
