# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Ian Mejias
#
# Distributed under terms of the GNU AGPLv3 license.

from .base import FunctionalTest, wait
from django.test import tag

class BootstrapLayoutTesting(FunctionalTest):
    def test_home_is_loading_correct_css(self):
        # juanito se dirige a la página principal y ve el contador del próximo
        # feriado centrado en la página.
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        @wait(10)
        def get_main_container():
            return self.browser.find_element_by_tag_name('main')

        main_container = get_main_container()

        self.assertAlmostEqual(
            main_container.location['x'] + main_container.size['width']/2,
            self.browser.get_window_size()['width']/2,
            delta=10
        )
