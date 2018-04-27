from .base import FunctionalTest

class BootstrapLayoutTesting(FunctionalTest):
    def test_home_is_loading_correct_css(self):
        # juanito se dirige a la página principal y ve el contador del próximo
        # feriado centrado en la página.
        self.browser.set_window_size(1024, 768)
        main_container = self.browser.find_element_by_css_selector('main')

        self.assertAlmostEqual(
            main_container.location['x'] + main_container.size['width']/2,
            self.browser.get_window_size()['width']/2,
            delta=10
        )
