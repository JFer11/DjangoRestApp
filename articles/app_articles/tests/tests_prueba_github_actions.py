import io

from rest_framework.test import APIClient, APITestCase
from rest_framework.parsers import JSONParser

from ..models import CustomUser, Article

"""
This file was created because we want to try CI/CD with Git Hub actions, and 
tests from other fiels are no longer updated. As a result, most of them fail and a CI would not be possible.
 
In order to use take advantage of the others tests, we have to update its assertions and finally change the file
names. Because Django will not recognized them if said files do not start with tests_ (or test_, i dont remember) 
"""


# python manage.py test app_articles.tests.tests_users.UserRegistrationTestCase
class UserRegistrationTestCase(APITestCase):
    """
    @classmethod
    def setUpClass(cls):
        # APITestCase includes a self.client, so it is not necessary to define it here
        # cls.client = APIClient()
        pass
    """

    @classmethod
    def tearDownClass(cls):
        CustomUser.objects.all().delete()
        Article.objects.all().delete()
        super().tearDownClass()

    def test_create_user(self):
        user_data = {
            "username": "Pablo",
            "email": "Pablo@g.com",
            "gender": "M",
            "birth": "2000-12-12T06:55:00Z",
            "level": "SR",
            "password": "Pablo"
        }
        response = self.client.post('/users/', user_data, format='json')

        self.assertEqual(response.status_code, 201)

    def test_try_create_user_missing_fields(self):
        user_data = {
            "username": "Pablo"
        }
        response = self.client.post('/users/', user_data, format='json')

        self.assertEqual(response.status_code, 400)

    def test_try_create_user_twice(self):
        user_data = {
            "username": "Pablo",
            "email": "Pablo@g.com",
            "gender": "M",
            "birth": "2000-12-12T06:55:00Z",
            "level": "SR",
            "password": "Pablo"
        }
        response_1 = self.client.post('/users/', user_data, format='json')
        response_2 = self.client.post('/users/', user_data, format='json')

        self.assertEqual(response_1.status_code, 201)
        self.assertEqual(response_2.status_code, 400)

    def test_try_create_user_no_request_body(self):
        response = self.client.post('/users/', format='json')
        self.assertEqual(response.status_code, 400)