import io

from rest_framework.test import APIClient, APITestCase
from rest_framework.parsers import JSONParser

from ..models import CustomUser, Article

"""
TO add any type of header, we have to add them in the request method as a key word argument.
Example:
response = self.client.get('/users/', **{'HTTP_AUTHORIZATION': 'Token dsg5sdf4gsd5f46sd4sdf54s'})

Note: is important to put the HTTP_ before the name of the header, The answer why we have to 
do this is extremely poorly documented, but it seems django does its own parsing of the headers passed in.
"""


# python manage.py test app_articles.tests.tests_users.UserRegistrationTestCase
class UserRegistrationTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        # APITestCase includes a self.client, so it is not necessary to define it here
        # cls.client = APIClient()
        pass

    @classmethod
    def tearDownClass(cls):
        CustomUser.objects.all().delete()
        Article.objects.all().delete()

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


# python manage.py test app_articles.tests.tests_users.UserLoginTestCase
class UserLoginTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        client = APIClient()
        user_data = {
            "username": "Pablo",
            "email": "Pablo@g.com",
            "gender": "M",
            "birth": "2000-12-12T06:55:00Z",
            "level": "SR",
            "password": "Pablo"
        }
        client.post('/users/', user_data, format='json')

    @classmethod
    def tearDownClass(cls):
        CustomUser.objects.all().delete()
        Article.objects.all().delete()

    def test_login_user(self):
        credentials = {
            "username": "Pablo",
            "password": "Pablo"
        }
        response = self.client.post('/api/login/', credentials, format='json')
        self.assertEqual(200, response.status_code)

    def test_try_login_user_bad_username(self):
        credentials = {
            "username": "Non-existent Username",
            "password": "Pablo"
        }
        response = self.client.post('/api/login/', credentials, format='json')
        self.assertEqual(400, response.status_code)

    def test_try_login_user_bad_password(self):
        credentials = {
            "username": "Pablo",
            "password": "Non-existent password"
        }
        response = self.client.post('/api/login/', credentials, format='json')
        self.assertEqual(400, response.status_code)

    def test_try_login_no_body(self):
        response = self.client.post('/api/login/', format='json')
        self.assertEqual(400, response.status_code)


# python manage.py test app_articles.tests.tests_users.GetAllUsersTestCase
class GetAllUsersTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        client = APIClient()
        user_data = {
            "username": "Pablo",
            "email": "Pablo@g.com",
            "gender": "M",
            "birth": "2000-12-12T06:55:00Z",
            "level": "SR",
            "password": "Pablo"
        }
        client.post('/users/', user_data, format='json')
        credentials = {
            "username": "Pablo",
            "password": "Pablo"
        }
        response = client.post('/api/login/', credentials, format='json')
        cls.token = response.json()['token']

    @classmethod
    def tearDownClass(cls):
        CustomUser.objects.all().delete()
        Article.objects.all().delete()

    def test_get_all_users(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get('/users/')

        is_pablo = False
        for user in response.json()['results']:
            if user['username'] == 'Pablo':
                is_pablo = True

        self.assertTrue(is_pablo)

    def test_try_get_all_users_no_credentials(self):
        response = self.client.get('/users/')

        stream = io.BytesIO(response.content)
        detail = JSONParser().parse(stream)['detail']
        self.assertEqual(detail, 'Authentication credentials were not provided.')
        self.assertEqual(401, response.status_code)


# python manage.py test app_articles.tests.tests_users.GetOneUserTestCase
class GetOneUserTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        client = APIClient()
        user_data = {
            "username": "Pablo",
            "email": "Pablo@g.com",
            "gender": "M",
            "birth": "2000-12-12T06:55:00Z",
            "level": "SR",
            "password": "Pablo"
        }
        client.post('/users/', user_data, format='json')
        credentials = {
            "username": "Pablo",
            "password": "Pablo"
        }
        response = client.post('/api/login/', credentials, format='json')
        cls.token = response.json()['token']

    @classmethod
    def tearDownClass(cls):
        CustomUser.objects.all().delete()
        Article.objects.all().delete()

    def test_get_one_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get('/users/Pablo/')

        username = response.json()['username']
        self.assertEqual(username, 'Pablo')
        self.assertEqual(response.status_code, 200)

    def test_try_get_one_user_no_credentials(self):
        response = self.client.get('/users/Pablo/')

        detail = response.json()['detail']
        self.assertEqual(detail, 'Authentication credentials were not provided.')
        self.assertEqual(401, response.status_code)

    def test_try_get_one_user_bad_username(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get('/users/NoUser/')

        self.assertEqual(404, response.status_code)


# python manage.py test app_articles.tests.tests_users.EditOneUserTestCase
class EditOneUserTestCase(APITestCase):
    def setUp(self):
        """
        Code below does not go in a setUpClass because I will edit the user, so I want to create it again from
        scratch for the next test.
        """
        user_data = {
            "username": "Pablo",
            "email": "Pablo@g.com",
            "gender": "M",
            "birth": "2000-12-12T06:55:00Z",
            "level": "SR",
            "password": "Pablo",
            "is_staff": True
        }
        self.client.post('/users/', user_data, format='json')
        credentials = {
            "username": "Pablo",
            "password": "Pablo"
        }
        response = self.client.post('/api/login/', credentials, format='json')
        self.token = response.json()['token']

    # TODO: Why don't I need a tearDown to delete the user?

    @classmethod
    def tearDownClass(cls):
        CustomUser.objects.all().delete()
        Article.objects.all().delete()

    def test_edit_one_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        new_user_data = {
            "username": "New Pablo",
            "email": "NewPablo@g.com",
            "gender": "F",
            "birth": "2000-12-12T06:55:00Z",
            "level": "MID",
            "password": "New Pablo"
        }
        response = self.client.put('/users/Pablo/', new_user_data)
        stream = io.BytesIO(response.content)
        user = JSONParser().parse(stream)
        for field in new_user_data:
            if field != 'password':
                self.assertEqual(user[field], new_user_data[field])

    def test_try_edit_one_user_no_body(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        new_user_data = {}

        response = self.client.put('/users/Pablo/', new_user_data)

        self.assertEqual(response.content, b'{"username":["This field is required."],"email":["This field is '
                                           b'required."],"gender":["This field is required."],"birth":["This field is '
                                           b'required."],"level":["This field is required."],"password":["This field '
                                           b'is required."]}')
        self.assertEqual(response.status_code, 400)

    def test_try_edit_one_user_bad_field(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        new_user_data = {
            "username": "New Pablo",
            "email": "BAD EMAIL",
            "gender": "BAD GENDER",
            "birth": "BAD BIRTH",
            "level": "BAD LEVEL",
            "password": "New Pablo"
        }
        response = self.client.put('/users/Pablo/', new_user_data)
        self.assertEqual(response.content, b'{"email":["Enter a valid email address."],"gender":["\\"BAD GENDER\\" is '
                                           b'not a valid choice."],"birth":["Datetime has wrong format. Use one of '
                                           b'these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]]['
                                           b'+HH:MM|-HH:MM|Z]."],"level":["\\"BAD LEVEL\\" is not a valid choice."]}')
        self.assertEqual(response.status_code, 400)

    def test_try_edit_one_user_bad_username_url(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        new_user_data = {
            "username": "New Pablo",
            "email": "NewPablo@g.com",
            "gender": "F",
            "birth": "2000-12-12T06:55:00Z",
            "level": "MID",
            "password": "New Pablo"
        }
        response = self.client.put('/users/bad_username/', new_user_data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'detail': 'Not found.'})

    def test_try_edit_one_user_already_used_username(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        new_user_data = {
            "username": "New Pablo",
            "email": "NewPablo@g.com",
            "gender": "F",
            "birth": "2000-12-12T06:55:00Z",
            "level": "MID",
            "password": "New Pablo"
        }
        self.client.post('/users/', new_user_data)
        response = self.client.put('/users/Pablo/', new_user_data)
        self.assertEqual(response.json(), {'username': ['custom user with this username already exists.'],
                                           'email': ['custom user with this email address already exists.']})


# python manage.py test app_articles.tests.tests_users.DeleteOneUserTestCase
class DeleteOneUserTestCase(APITestCase):
    def setUp(self):
        """
        Code below does not go in a setUpClass because I will delete the user, so I want to create it again from
        scratch for the next test.
        """
        user_data = {
            "username": "Pablo",
            "email": "Pablo@g.com",
            "gender": "M",
            "birth": "2000-12-12T06:55:00Z",
            "level": "SR",
            "password": "Pablo",
            "is_staff": True
        }
        user = self.client.post('/users/', user_data, format='json')
        self.id_user = user.json()['id']

        credentials = {
            "username": "Pablo",
            "password": "Pablo"
        }
        response = self.client.post('/api/login/', credentials, format='json')
        self.token = response.json()['token']

    @classmethod
    def tearDownClass(cls):
        CustomUser.objects.all().delete()
        Article.objects.all().delete()

    def test_delete_one_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f'/users/{self.id_user}/')
        self.assertEqual(204, response.status_code)

    def test_try_delete_one_user_twice(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response_1 = self.client.delete(f'/users/{self.id_user}/')
        response_2 = self.client.delete(f'/users/{self.id_user}/')
        self.assertEqual(204, response_1.status_code)
        # One the user is deleted (because we are deleting ourselves), we do not have the permissions to
        # delete another user, so that is why a 401 is returned instead of a 404.
        self.assertEqual(401, response_2.status_code)

    def test_try_delete_non_existent_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete('/users/NON-EXISTENT-ID/')
        self.assertEqual(404, response.status_code)

    def test_try_delete_a_user_no_token(self):
        response = self.client.delete(f'/users/{self.id_user}/')
        self.assertEqual(401, response.status_code)


# python manage.py test app_articles.tests.tests_users.PartialModifyOneUserTestCase
class PartialModifyOneUserTestCase(APITestCase):
    def setUp(self):
        """
        Code below does not go in a setUpClass because I will edit the user, so I want to create it again from
        scratch for the next test.
        """
        self.user_data = {
            "username": "Pablo",
            "email": "Pablo@g.com",
            "gender": "M",
            "birth": "2000-12-12T06:55:00Z",
            "level": "SR",
            "password": "Pablo",
            "is_staff": True
        }
        self.client.post('/users/', self.user_data, format='json')
        credentials = {
            "username": "Pablo",
            "password": "Pablo"
        }
        response = self.client.post('/api/login/', credentials, format='json')
        self.token = response.json()['token']

    @classmethod
    def tearDownClass(cls):
        CustomUser.objects.all().delete()
        Article.objects.all().delete()

    def test_partial_modify_one_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        update_field = {
            "gender": "F",
            "password": "newpassword"
        }
        response = self.client.patch('/users/Pablo/', update_field, format='json')

        self.assertEqual(200, response.status_code)
        for field in self.user_data:
            if field not in ['gender', 'password', 'is_staff']:
                self.assertEqual(self.user_data[field], response.json()[field])
            elif field == 'gender':
                self.assertEqual(response.json()[field], "F")

    def test_try_partial_modify_a_user_unique_field_already_used(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        new_user_data = {
            "username": "Nicolas",
            "email": "Nicolas@g.com",
            "gender": "F",
            "birth": "2000-12-12T06:55:00Z",
            "level": "JR",
            "password": "Pablo"
        }
        self.client.post('/users/', new_user_data, format='json')

        update_field = {
            "username": new_user_data["username"],
            "gender": "F",
            "password": "new_password"
        }
        response = self.client.patch('/users/Pablo/', update_field, format='json')

        self.assertEqual(400, response.status_code)
        self.assertEqual(response.json(), {'username': ['custom user with this username already exists.']})

    def test_try_partial_modify_non_existent_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.patch('/users/NON-EXISTENT-ID/', {})
        self.assertEqual(404, response.status_code)
