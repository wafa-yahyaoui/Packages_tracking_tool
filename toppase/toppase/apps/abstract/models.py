# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Template(models.Model):
    """This class Represents the Template class"""
    name = models.CharField(max_length=100)
    html = models.FileField()

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name


class LandingPage(Template):
    """This class represents the landing page class"""

    def __unicode__(self):
        return self.name


class TemplateEmail(Template):
    """This class represents the landing page class"""
    text = models.FileField()

    def __unicode__(self):
        return self.name
