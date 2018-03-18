# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from urlparse import urlparse


def get_hostname(url):
    parsed_uri = urlparse(url)
    return parsed_uri.netloc
