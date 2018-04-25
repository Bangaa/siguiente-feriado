from django.test import TestCase

class ViewsTests(TestCase):
    def test_home_uses_homeDotHtml_template(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
