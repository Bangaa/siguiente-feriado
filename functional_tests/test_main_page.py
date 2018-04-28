# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Ian Mejias
#
# Distributed under terms of the GNU AGPLv3 license.

from django.test import tag
from .base import FunctionalTest, wait
from datetime import date, timedelta, datetime
from feriados.models import Feriado

@wait(5)
def get_countdown_table(test):
    return test.browser.find_element_by_css_selector('table.countdown-table')

class FeriadoCounterTests(FunctionalTest):
    @tag('wip')
    def test_countdown_show_correct_time_till_next_feriado(self):
        """
        Juanito se encuentra en la pagina principal y, sabiendo que manyana
        es feriado, ve que el contador muestra el tiempo correcto que queda
        para que empiece el dia feriado.
        """
        tomorrow = date.today() + timedelta(days=1)
        Feriado.objects.create(fecha=tomorrow)

        # Juanito mira el contador que aparece en la pagina principal
        self.browser.get(self.live_server_url)
        table = get_countdown_table(self)
        cd_page_elements = table.find_elements_by_css_selector('tbody td') # [<webelm>, ... , <webelm>]
        cd_page_elements = [int(dom.text) for dom in cd_page_elements]   # [<int>, ..., <int>]

        delta_pagina = dict(zip(
            ['dias', 'horas', 'minutos'],
            cd_page_elements
        ))
        # ... y calcula por su cuenta cuanto falta para el feriado

        delta_juanito = datetime(*tomorrow.timetuple()[:6]) - datetime.now()

        # primero compara los dias

        self.assertEqual(delta_pagina['dias'], delta_juanito.days)

        # y luego compara los minutos totales, con un margen de error (segun
        # lo que se haya demorado el en hacer el calculo: 1 minuto)

        minutos_pagina = delta_pagina['horas']*60 + delta_pagina['minutos']
        minutos_juanito = delta_juanito.seconds // 60

        self.assertAlmostEqual(minutos_pagina, minutos_juanito, delta=1)
