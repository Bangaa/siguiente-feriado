import unittest
import unittest.mock
from django.test import TestCase
from django.core.exceptions import ValidationError
from feriados.models import Feriado
from datetime import date, datetime

class ModelTests(TestCase):
    def test_cant_create_two_feriados_with_the_same_date(self):
        feriado1, feriado2 = Feriado(), Feriado()
        feriado1.fecha = feriado2.fecha = date.today()
        feriado1.save() # se guarda normalmente

        with self.assertRaises(ValidationError):
            feriado2.full_clean()

    def test_feriados_are_no_irrenunciables_by_default(self):
        f = Feriado.objects.create(fecha=date.today())
        self.assertEqual(f.es_irrenunciable, False)

    def test_cant_create_feriado_without_date(self):
        f = Feriado()
        self.assertRaises(ValidationError, f.full_clean)

    def test_year_manager_function_returns_as_expected(self):
        Feriado.objects.create(fecha=date(2018,1,1))
        Feriado.objects.create(fecha=date(2016,1,1))
        Feriado.objects.create(fecha=date(2016,2,1))

        fer2016 = Feriado.objects.year(2016)
        fer2018 = Feriado.objects.year(2018)

        self.assertEqual(fer2016.count(), 2)
        self.assertEqual(fer2018.count(), 1)

    def test_feriados_are_ordered_by_fecha(self):
        f1 = Feriado.objects.create(fecha='2032-01-27')
        f2 = Feriado.objects.create(fecha='2032-01-02')
        f3 = Feriado.objects.create(fecha='2032-01-15')

        lista = Feriado.objects.all()

        self.assertEqual(list(lista), [f2,f3,f1])

from feriados.models import DeltaFeriado
import pytz

class DeltaFeriadoTests(TestCase):
    def setUp(self):
        self.feriado = Feriado.objects.create(fecha=date(2018,7,2))

    @unittest.mock.patch('feriados.models.datetime')
    def test_gives_correct_time_difference(self, datetime_m):
        datetime_m.now = lambda *argv,**kwargs: datetime.now(*argv, **kwargs).replace(2018,7,1,23,15,1)
        datetime_m.side_effect = lambda *argv,**kwargs: datetime(*argv,**kwargs)

        fd = DeltaFeriado(self.feriado, 'Chile/Continental')

        self.assertEqual(fd.horas, 0)
        self.assertEqual(fd.minutos, 44)
