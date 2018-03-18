# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Order, OrderCSV, Product

# Register your models here.


admin.site.register(Order)
admin.site.register(OrderCSV)
admin.site.register(Product)
