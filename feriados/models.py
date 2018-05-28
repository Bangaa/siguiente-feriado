# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Ian Mejias
#
# Distributed under terms of the GNU AGPLv3 license.


from django.db import models

class FeriadoManager(models.Manager):
    def year(self, esp_year):
        return super().get_queryset().filter(fecha__year=str(esp_year))

class Feriado(models.Model):
    """Representacion de un feriado.
    Los campos son los "mismos" que en la tabla de feriados de la página
    www.feriados.cl:
      1 Fecha
      2 Festividad
      3 Tipo de feriado
      4 Es irrenunciable
      5 Respaldo legal (ley)
    """
    CIVIL = 'C'
    RELIGIOSO = 'R'
    TIPOS_FERIADO = (
        (CIVIL, 'Civil'),
        (RELIGIOSO, 'Religioso'),
    )

    fecha = models.DateField(unique=True, null=True)
    festividad = models.CharField(max_length=50, blank=True)
    es_irrenunciable = models.BooleanField(default=False)
    tipo = models.CharField(
        max_length=1,
        choices=TIPOS_FERIADO,
        default=CIVIL
    )

    objects = FeriadoManager()

    class Meta:
        ordering = ('fecha',)

from datetime import datetime
import pytz

class DeltaFeriado(object):
    def __init__(self, feriado, timezone='UTC'):
        if feriado is None:
            return None
        tz_chile = pytz.timezone('Chile/Continental')
        delta = datetime(*feriado.fecha.timetuple()[:6], tzinfo=tz_chile) - datetime.now(tz=pytz.timezone(timezone))
        self.dias = delta.days
        self.horas = delta.seconds // 3600
        self.minutos = delta.seconds%3600 // 60

