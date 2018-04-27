# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Ian Mejias
#
# Distributed under terms of the GNU AGPLv3 license.

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from feriados.models import Feriado
from feriados.serializers import FeriadoSerializer


@csrf_exempt
## GET /api/feriados/<year>/
def list(request, year):
    if request.method == 'GET':
        feriados = Feriado.objects.year(year)
        serializer = FeriadoSerializer(feriados, many=True)
        return JsonResponse(serializer.data, safe=False)
    return HttpResponse(status=400)
