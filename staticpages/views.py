# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Ian Mejias
#
# Distributed under terms of the GNU AGPLv3 license.


from django.shortcuts import render
from feriados.models import Feriado, DeltaFeriado
from datetime import date

def home(request):
    feriado = Feriado.objects.filter(fecha__gt=date.today()).first()
    delta = DeltaFeriado(feriado, 'Chile/Continental')
    return render(request, 'home.html', context={'feriado': feriado, 'delta':delta})
