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

@tag('wip')
class ViewListTests(TestCase):
    def test_can_retrieve_all_feriados_from_api(self):
        """Testing GET /api/feriados/ """
        Feriado.objects.create(fecha=date(2018,5,21))
        Feriado.objects.create(fecha=date(2018,1,1))

        response = self.client.get('/api/feriados/')
        self.assertEqual(response.status_code, 200)
        lista = eval(response.content)
        self.assertEqual(len(lista), 2)

    def test_can_retrieve_specific_feriado(self):
        """Testing GET /api/feriados/<feriado_id>/ """
        fs = [
            Feriado.objects.create(fecha=date(2018,5,21), festividad='21 de mayo'),
            Feriado.objects.create(fecha=date(2018,1,1), festividad='Año nuevo'),
        ]

        for i in range(2):
            url = "/api/feriados/{id}/".format(id=i+1)
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                feriado = eval(response.content)
                self.assertEqual(feriado.get('festividad'), fs[i].festividad)

    @unittest.skip
    def test_cant_POST_duplicated_feriados(self):
        self.client.post('/api/feriados/', data={'fecha': '2018-05-01'})
        response = self.client.post('/api/feriados/', data={'fecha': '2018-05-01'})
        self.assertEqual(response.status_code, 400) # bad request

        self.assertEqual(Feriado.objects.count(), 1)
        self.assertEqual(Feriado.objects.first().fecha, date(2018, 5, 1))

