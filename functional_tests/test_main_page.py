# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Ian Mejias
#
# Distributed under terms of the GNU AGPLv3 license.

from django.test import tag
from .base import FunctionalTest, wait, wait_for
from datetime import date, timedelta, datetime
from feriados.models import Feriado
import pytz

class FeriadoCounterTests(FunctionalTest):
    def test_countdown_show_correct_time_till_next_feriado(self):
        """Contador debe estar correcto.
        Juanito se encuentra en la pagina principal y, sabiendo que manyana
        es feriado, ve que el contador muestra el tiempo correcto que queda
        para que empiece el dia feriado.
        """
        tomorrow = date.today() + timedelta(days=1)
        Feriado.objects.create(fecha=tomorrow)

        # Juanito mira el contador que aparece en la pagina principal
        self.browser.get(self.live_server_url)
        table = self.get_countdown_table()
        cd_page_elements = table.find_elements_by_css_selector('tbody td') # [<webelm>, ... , <webelm>]
        cd_page_elements = [int(dom.text) for dom in cd_page_elements]   # [<int>, ..., <int>]

        delta_pagina = dict(zip(
            ['dias', 'horas', 'minutos'],
            cd_page_elements
        ))
        # ... y calcula por su cuenta cuanto falta para el feriado

        tzchile = pytz.timezone("Chile/Continental")
        delta_juanito = tzchile.localize(datetime(*tomorrow.timetuple()[:3])) - datetime.now(tzchile)

        # primero compara los dias

        self.assertEqual(delta_pagina['dias'], delta_juanito.days, "Dias no coinciden")

        # y luego compara los minutos totales, con un margen de error (segun
        # lo que se haya demorado el en hacer el calculo: 1 minuto)

        minutos_pagina = delta_pagina['horas']*60 + delta_pagina['minutos']
        minutos_juanito = delta_juanito.seconds // 60

        self.assertAlmostEqual(minutos_pagina, minutos_juanito, delta=1, msg="Cantidad de minutos no coinciden")

    @tag('wip')
    def test_home_link_from_page_404(self):
        """Puedo volver al 'Home page' haciendo click en 'Home'.
        Juanito se equivoca de URL, pero puede volver al Home haciendo click
        en el link Home
        """
        # Juanito se equivoca al tipear.
        self.browser.get(self.live_server_url + "/api/feriado/2018/")

        # Le aparece el mensaje error 404.
        h1 = wait_for(lambda: self.browser.find_element_by_css_selector('h1'))
        self.assertEqual(h1.text, "Error 404")

        # Hace click en el link 'Home' de la barra de navegacion y lo redirige
        # a la pagina con el contador.

        home_link = wait_for(lambda:self.browser.find_element_by_link_text("Home"))
        home_link.click()

        self.get_countdown_table() # should not raise

    @wait(10)
    def get_countdown_table(self):
        return self.browser.find_element_by_css_selector('table.countdown-table')
