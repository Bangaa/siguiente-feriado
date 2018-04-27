# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Ian Mejias
#
# Distributed under terms of the GNU AGPLv3 license.


from django.core.exceptions import ObjectDoesNotExist
from feriados.models import Feriado
from rest_framework import serializers

class FeriadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feriado
        fields = ('id', 'fecha', 'festividad', 'es_irrenunciable', 'tipo')
