# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField

from ..accounts.models import Courier, StatusDelivery, Store, Client, Member


class Product(models.Model):
    sku = models.CharField(
        verbose_name=_('SKU'),
        unique=True,
        max_length=120,
        primary_key=True
    )
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=150
    )
    url = models.URLField(
        verbose_name=_('URL'),
        blank=True,
        null=True
    )
    url_image = models.URLField(
        verbose_name=_('URL IMAGE'),
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __unicode__(self):
        return str(self.sku)


class OrderCSV(models.Model):
    file_csv = models.FileField(upload_to='uploads/', error_messages={'required': 'Please enter a valid file!'})

    class Meta:
        verbose_name = _('Order CSV')
        verbose_name_plural = _('Order CSV')

    def __unicode__(self):
        return str(self.id)


class Order(models.Model):
    store = models.ForeignKey(Store,
                              related_name='orders',
                              on_delete=models.CASCADE)
    file_csv = models.ForeignKey(
        OrderCSV,
        null=True,
        blank=True
    )
    client = models.ForeignKey(Client)
    status =models.CharField(
        verbose_name=_('Status'),
        max_length=120,
    )
    #TODO : change the status field
    # status = models.ForeignKey(StatusDelivery)
    tracking_id = models.CharField(
        verbose_name=_('Tracking Id'),
        max_length=150,
    )
    courier = models.ForeignKey(Courier)
    origin = models.CharField(
        verbose_name=_('  place'),
        max_length=120,
        null=True,
        blank=True
    )
    destination = models.CharField(
        verbose_name=_('Destination place'),
        max_length=120,
        null=True,
        blank=True
    )
    date_estimation = models.DateField(
        null=True,
        blank=True
    )
    products = models.ManyToManyField(
        Product,
        related_name= "orders",
        null=True,
        blank=True,
    )
    rate = models.IntegerField(
        verbose_name=_('Rate'),
        default=0,
        null=True,
        blank=True
    )
    note = models.TextField(
        verbose_name=_('Note'),
        help_text=_('Add a note'),
        null=True,
        blank=True
    )
    date_created = models.DateTimeField(
        verbose_name=_('date Created'),
        default=timezone.now
    )
    owner = models.ForeignKey(Member,
                              related_name='orders',
                              on_delete=models.CASCADE)

    reason= models.TextField(
        verbose_name=_('Reason'),
        help_text=_('Add reason'),
        null=True,
        blank=True
    )

    events_history = JSONField(null=True, blank=True)
    accept_test_flag = models.BooleanField(default=True)

    class Meta:
        # unique_together = ('client', 'store')
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __unicode__(self):
        return str(self.id)
