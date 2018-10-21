from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseRedirect
from django.test import TestCase, RequestFactory

from snippets.views import new_snippet

UserModel = get_user_model()


class SnippetCreateViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserModel.objects.create_user(
            username='c-bata', email='shibata@example.com', password='secret')

    def test_should_return_200_if_sending_get_request(self):
        request = self.factory.get("/endpoint/of/create_snippet")
        request.user = self.user
        response = new_snippet(request)
        self.assertEqual(response.status_code, 200)

    def test_should_redirect_if_user_does_not_login(self):
        request = self.factory.get("/endpoint/of/create_snippet")
        request.user = AnonymousUser()
        response = new_snippet(request)
        self.assertIsInstance(response, HttpResponseRedirect)

    def test_should_return_400_if_sending_empty_post_request(self):
        request = self.factory.post("/endpoint/of/create_snippet", data={})
        request.user = self.user
        response = new_snippet(request)
        self.assertEqual(response.status_code, 400)

    def test_should_return_201_if_sending_valid_post_request(self):
        request = self.factory.post("/endpoint/of/create_snippet", data={
            'title': 'hello world',
            'code': 'print("Hello World")',
            'description': 'Just printing "Hello World"',
        })
        request.user = self.user
        response = new_snippet(request)
        self.assertIsInstance(response, HttpResponseRedirect)
