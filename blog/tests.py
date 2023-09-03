from django.test import TestCase
from django.contrib.auth import get_user_model


class BlogAccessTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='sky_pro2023@mail.ru',
            password='9MoXf1JU4RBp',
        )

    def test_moderator_access_to_protected_view(self):
        # Ваш код для тестирования доступа к защищенным представлениям для модераторов
        response = self.client.get('/blog/create/')
        self.assertEqual(response.status_code, 200)


