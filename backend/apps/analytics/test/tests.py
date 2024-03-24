from django.test import TestCase
from myapp.views import HomePageView

class HomePageViewTest(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_home_page_content(self):
        response = self.client.get('/')
        self.assertContains(response, "Welcome to my website!")

