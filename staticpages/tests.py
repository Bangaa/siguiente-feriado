import unittest
import unittest.mock
from django.test import TestCase
from feriados.models import Feriado
from datetime import date, timedelta

class HomeViewTests(TestCase):
    @unittest.mock.patch('staticpages.views.Feriado')
    @unittest.mock.patch('staticpages.views.DeltaFeriado')
    def test_home_uses_homeDotHtml_template(self, DeltaFeriado_m, Feriado_m):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_home_controller_passes_a_Feriado(self):
        Feriado.objects.create(fecha='2032-01-01')
        response = self.client.get('/')
        self.assertEqual(type(response.context['feriado']), Feriado)

    def test_home_controller_passes_correct_Feriado(self):
        yesterday = Feriado.objects.create(fecha=(date.today() - timedelta(days=1)))
        dayaftertom = Feriado.objects.create(fecha=(date.today() + timedelta(days=2)))
        tomorrow = Feriado.objects.create(fecha=(date.today() + timedelta(days=1)))

        response = self.client.get('/')
        self.assertEqual(response.context['feriado'], tomorrow)

    @unittest.mock.patch('staticpages.views.Feriado')
    @unittest.mock.patch('staticpages.views.DeltaFeriado')
    def test_home_controller_passes_a_DeltaFeriado_object(
        self, DeltaFeriado_m, Feriado_m
    ):
        feriado = Feriado_m.objects.filter().first.return_value
        delta = DeltaFeriado_m.return_value
        response = self.client.get('/')
        DeltaFeriado_m.assert_called_once_with(feriado)

        self.assertEqual(response.context['delta'], delta)

    @unittest.mock.patch('staticpages.views.Feriado')
    def test_home_passes_none_as_feriado_if_there_is_no_feriados_created(self, Feriado_m):
        Feriado_m.objects.filter().first.return_value = None
        response = self.client.get('/')
        self.assertIsNone(response.context['feriado'])

class ErrorPagesTets(TestCase):
    def test_non_existing_urls_render_404DotHtml_template(self):
        response = self.client.get('/haslkdhashdkasjhkjhdoesnt_exist')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

