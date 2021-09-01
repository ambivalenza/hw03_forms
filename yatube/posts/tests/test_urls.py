from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from ..models import Group

User = get_user_model()


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создадим запись в БД для проверки доступности адреса task/test-slug/
        Group.objects.create(
            title='Тестовый заголовок',
            slug='test-slug',
            description='Тестовый текст',
        )

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем пользователя
        self.user = User.objects.create_user(username='HasNoName')
        # Создаем второй клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)

    def test_homepage(self):
        # Отправляем запрос через client,
        # созданный в setUp()
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_group_post_page(self):
        response = self.guest_client.get('/group/<slug:slug>/')
        self.assertEqual(response.status_code, 404)

    def test_profile_page(self):
        response = self.guest_client.get('/<str:username>/')
        self.assertEqual(response.status_code, 404)

    def test_profile_post_page(self):
        response = self.guest_client.get('/<str:username>/<int:post_id>/')
        self.assertEqual(response.status_code, 404)

    def test_create_new_post_page(self):
        response = self.authorized_client.get('/new/')
        self.assertEqual(response.status_code, 200)

    def test_post_edit_page(self):
        response = self.authorized_client.get('/<str:username>/<int:post_id>/edit/')
        self.assertEqual(response.status_code, 404)

    # def test_edit_delete_redirect(self):
    #     form_data = {'text': 'Смена текста'}
    #     response = self.authorized_client.post(
    #         reverse('posts:post_edit', kwargs={'post_id': self.post_id}),
    #         data=form_data
    #     )
    #     self.assertEqual(response.status_code, 302)
    # def test_create_new_post_page_redirect_anonymous(self):
    # """Страница /task/ перенаправляет анонимного пользователя."""
    #  response = self.guest_client.get('/new/', follow=True)
    # self.assertRedirects(
    # response, '/admin/login/?next=/new/'
    # )

    # def test_post_edit_page_redirect_anonymous(self):
    #   """Страница /task/ перенаправляет анонимного пользователя."""
    #   response = self.guest_client.get('/<str:username>/<int:post_id>/edit/', follow=True)
    #   self.assertRedirects(
    #       response, '/admin/login/?next=/<str:username>/<int:post_id>/edit/'
    #  )

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Шаблоны по адресам
        templates_url_names = {
            'index.html': '/',
            # 'posts/new.html': '/new/',
            # 'posts/group.html': '/group/<slug:slug>/',
            # 'posts/profile.html': '/<str:username>/',
            # 'posts/post.html': '/<str:username>/<int:post_id>/',
            # 'posts/new.html': '/<str:username>/<int:post_id>/edit/',

        }
        for template, adress in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertTemplateUsed(response, template)
