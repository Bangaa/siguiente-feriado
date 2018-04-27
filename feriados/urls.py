# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Ian Mejias
#
# Distributed under terms of the GNU AGPLv3 license.


from django.urls import path, re_path
from feriados import views

urlpatterns = [
    re_path(r'(?P<year>\d{4})/', views.list),
]
