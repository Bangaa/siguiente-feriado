# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Ian Mejias
#
# Distributed under terms of the GPL license.

from django.test import TestCase, tag
import unittest
from feriados.models import Feriado
from datetime import date

false = False   # para poder convertir el contenido que devuelve la api

class ViewListTests(TestCase):
    def test_can_retrieve_all_feriados_of_a_year(self):
        """Testing GET /api/feriados/search? """
        Feriado.objects.create(fecha=date(2018,5,21))
        Feriado.objects.create(fecha=date(2019,1,1))
        Feriado.objects.create(fecha=date(2018,1,1))

        response = self.client.get('/api/feriados/2018/')
        self.assertEqual(response.status_code, 200)
        lista = eval(response.content)
        self.assertEqual(len(lista), 2)

    def test_cant_POST(self):
        response = self.client.post('/api/feriados/2018/', data={'fecha': '2018-05-01'})
        self.assertEqual(response.status_code, 400) # bad request

