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


import io
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.hashers import check_password
from main.models import User


class RegistrationTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def _create_test_image(self):
        file_obj = io.BytesIO()
        image = Image.new('RGB', (100, 100), color='blue')
        image.save(file_obj, format='PNG')
        file_obj.seek(0)
        return SimpleUploadedFile('test_avatar.png', file_obj.read(), content_type='image/png')

    def test_register_page_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/register.html')
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'name="password"')
        self.assertContains(response, 'name="avatar"')

    def test_register_success_without_avatar(self):
        response = self.client.post(reverse('register'), {
            'username': 'john_doe',
            'email': 'john@example.com',
            'password': 'secretpassword123'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')

        user = User.objects.get(username='john_doe')
        self.assertEqual(user.email, 'john@example.com')
        self.assertTrue(check_password('secretpassword123', user.password))
        self.assertFalse(bool(user.avatar))

    def test_register_success_with_avatar(self):
        avatar = self._create_test_image()
        response = self.client.post(reverse('register'), {
            'username': 'jane_doe',
            'email': 'jane@example.com',
            'password': 'secretpassword123',
            'avatar': avatar
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')

        user = User.objects.get(username='jane_doe')
        self.assertTrue(bool(user.avatar))
        self.assertTrue(user.avatar.name.startswith('avatars/'))
        # Clean up file created by test
        if user.avatar:
            user.avatar.delete(save=False)

    def test_register_duplicate_username(self):
        User.objects.create(username='existing_user', email='first@example.com', password='123')
        response = self.client.post(reverse('register'), {
            'username': 'existing_user',
            'email': 'second@example.com',
            'password': '123'
        })
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data['status'], 'error')
        self.assertIn("ім'ям вже існує", data['message'])

    def test_register_duplicate_email(self):
        User.objects.create(username='user1', email='same@example.com', password='123')
        response = self.client.post(reverse('register'), {
            'username': 'user2',
            'email': 'same@example.com',
            'password': '123'
        })
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data['status'], 'error')
        self.assertIn("поштою вже існує", data['message'])

    def test_register_missing_fields(self):
        response = self.client.post(reverse('register'), {
            'username': '',
            'email': 'test@example.com',
            'password': ''
        })
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data['status'], 'error')

