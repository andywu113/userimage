#coding=utf-8
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj_configure.settings")
django.setup()

from django.conf.urls import url
from .views import *

urlpatterns = [
        url(r'^principleCurve/$',principleCurve),
        url(r'^companiesCluster/$', companiesCluster),

]

