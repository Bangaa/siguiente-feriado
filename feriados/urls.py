# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Ian Mejias
#
# Distributed under terms of the GPL license.

from django.urls import path
from feriados import views

urlpatterns = [
    path('', views.list),
    path('<int:feriado_id>/', views.detail),
]
