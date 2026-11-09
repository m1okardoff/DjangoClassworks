from django.test import TestCase, Client
from django.urls import reverse


class SearchCardTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page_contains_search_form(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form action="/search/"')
        self.assertContains(response, 'name="name"')

    def test_search_existing_card_exact(self):
        response = self.client.get(reverse('search'), {'name': 'Розділ 1'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/card.html')
        self.assertContains(response, 'Розділ 1')
        self.assertContains(response, 'django.png')

    def test_search_existing_card_case_insensitive(self):
        response = self.client.get(reverse('search'), {'name': 'розділ 2'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/card.html')
        self.assertContains(response, 'Розділ 2')
        self.assertContains(response, 'fastapi.png')

    def test_search_existing_card_partial(self):
        response = self.client.get(reverse('search'), {'name': '3'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/card.html')
        self.assertContains(response, 'Розділ 3')
        self.assertContains(response, 'flask.png')

    def test_search_by_q_parameter(self):
        response = self.client.get(reverse('search'), {'q': 'Розділ 1'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/card.html')
        self.assertContains(response, 'Розділ 1')

    def test_search_card_not_found(self):
        response = self.client.get(reverse('search'), {'name': 'Невідь-що'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/not_found.html')
        self.assertContains(response, 'Картку не знайдено')
        self.assertContains(response, 'Невідь-що')

    def test_search_card_empty_query(self):
        response = self.client.get(reverse('search'), {'name': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/not_found.html')

    def test_search_post_request(self):
        response = self.client.post(reverse('search'), {'name': 'Розділ 1'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/card.html')
        self.assertContains(response, 'Розділ 1')

    def test_search_by_url_path(self):
        response = self.client.get('/search/Розділ 1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/card.html')
        self.assertContains(response, 'Розділ 1')

    def test_get_card_by_id(self):
        response = self.client.get('/card/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/card.html')
        self.assertContains(response, 'Розділ 1')

    def test_get_card_by_invalid_id(self):
        response = self.client.get('/card/999/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/not_found.html')
