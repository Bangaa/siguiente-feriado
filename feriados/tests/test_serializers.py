#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Ian Mejias
#
# Distributed under terms of the GPL license.


from datetime import date
import unittest
from feriados.serializers import FeriadoSerializer
from feriados.models import Feriado

class FeriadoSerializerTests(unittest.TestCase):
    def test_serializer_cannot_save_duplicated_feriados(self):
        fecha = date.today()
        Feriado.objects.create(fecha=fecha)
        data = {'fecha': fecha.isoformat()}

        serializer = FeriadoSerializer(data=data)
        self.assertFalse(serializer.is_valid(), 'Se puede guardar una fecha invalida')
