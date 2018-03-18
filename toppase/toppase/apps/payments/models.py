# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils import timezone

from ..accounts.models import Store

# TODO: PLAN_CHOICE
PLAN_CHOICE = (('free', 'Free'),
               ('strd', 'Standard'),
               ('prm', 'Premium'))


class Billing(models.Model):
    store = models.ForeignKey(Store)
    plan = models.CharField(
        verbose_name=_('Plan'),
        choices=PLAN_CHOICE,
        max_length=120
    )

    start_date = models.DateField(
        verbose_name=_('Start date'),
        default=timezone.now
    )
    active = models.BooleanField(
        verbose_name=_('Active'),
        editable=False,
        default=True,
        help_text=_("this plan is  active ?")
    )

    period_count = models.IntegerField(
        verbose_name=_('Number of interval'),
        null=True,
        blank=True,
        default=1
    )

    class Meta:
        verbose_name_plural = _('Billing')
        verbose_name = _('Billing')
        ordering = ['start_date', ]
