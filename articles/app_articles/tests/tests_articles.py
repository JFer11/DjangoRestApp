import io
from rest_framework.test import APIClient, APITestCase
from rest_framework.parsers import JSONParser

from ..models import CustomUser, Article


# python manage.py test app_articles.tests.tests_articles.CreateArticleTestCase
class CreateArticleTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        client = APIClient()
        user_data = {
            "username": "Pablo",
            "email": "Pablo@g.com",
            "gender": "M",
            "birth": "2000-12-12T06:55:00Z",
            "level": "SR",
            "password": "Pablo",
            "is_staff": True
        }
        cls.id_user = client.post('/users/', user_data, format='json').json()['id']
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

    def test_create_an_article(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        article_json = {
            'title': "Title example",
            'text': 'Text example'
        }
        response = self.client.post('/articles/', article_json, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['title'], article_json['title'])
        self.assertEqual(response.json()['text'], article_json['text'])

    def test_try_create_article_missing_fields(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        article_json = {}
        response = self.client.post('/articles/', article_json, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'title': ['This field is required.'], 'text': ['This field is required.']})

    def test_try_create_an_article_twice(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        article_json = {
            'title': "Title example",
            'text': 'Text example'
        }
        response_1 = self.client.post('/articles/', article_json, format='json')
        response_2 = self.client.post('/articles/', article_json, format='json')
        self.assertEqual(response_1.status_code, 201)
        self.assertEqual(response_2.status_code, 400)


# python manage.py test app_articles.tests.tests_articles.GetAllArticlesTestCase
class GetAllArticlesTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        client = APIClient()
        user_data = {
            "username": "Pablo",
            "email": "Pablo@g.com",
            "gender": "M",
            "birth": "2000-12-12T06:55:00Z",
            "level": "SR",
            "password": "Pablo",
            "is_staff": True
        }
        cls.id_user = client.post('/users/', user_data, format='json').json()['id']
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

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        self.all_articles = []
        for i in range(0, 5):
            article_json = {
                'title': "Title example " + str(i),
                'text': 'Text example'
            }
            response = self.client.post('/articles/', article_json, format='json')
            self.all_articles.append(response.json())

    def test_get_all_articles(self):
        response = self.client.get('/articles/')

        self.assertEqual(self.all_articles, response.json()['results'])
        self.assertEqual(len(self.all_articles), response.json()['count'])
        self.assertEqual(200, response.status_code)

    def test_try_get_all_users_no_credentials(self):
        # in setUp credentials were setted, so now we have to remove them.
        self.client.credentials(HTTP_AUTHORIZATION='BAD TOKEN')
        response = self.client.get('/articles/')
        self.assertEqual(response.json()['detail'], 'Authentication credentials were not provided.')
        self.assertEqual(401, response.status_code)

    # TODO: FALTAN LOS DE GET ASC OR DESC


# python manage.py test app_articles.tests.tests_articles.GetOneArticleTestCase
class GetOneArticleTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        client = APIClient()
        user_data = {
            "username": "Pablo",
            "email": "Pablo@g.com",
            "gender": "M",
            "birth": "2000-12-12T06:55:00Z",
            "level": "SR",
            "password": "Pablo",
            "is_staff": True
        }
        cls.id_user = client.post('/users/', user_data, format='json').json()['id']
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

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        self.all_articles = []
        for i in range(0, 5):
            article_json = {
                'title': "Title example " + str(i),
                'text': 'Text example'
            }
            response = self.client.post('/articles/', article_json, format='json')
            self.all_articles.append(response.json())

    def test_get_one_article(self):
        article = self.all_articles[0]
        response = self.client.get(f'/articles/{article["id"]}/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), article)

    def test_try_get_one_article_no_credentials(self):
        # in setUp credentials were setted, so now we have to remove them.
        self.client.credentials(HTTP_AUTHORIZATION='BAD TOKEN')
        article = self.all_articles[0]
        response = self.client.get(f'/articles/{article["id"]}/')

        self.assertEqual('Authentication credentials were not provided.', response.json()['detail'])
        self.assertEqual(401, response.status_code)

    def test_try_get_one_article_bad_id(self):
        response = self.client.get('/articles/non_existent_article/')

        self.assertEqual(404, response.status_code)


# python manage.py test app_articles.tests.tests_articles.EditOneArticleTestCase
class EditOneArticleTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        client = APIClient()
        user_data = {
            "username": "Pablo",
            "email": "Pablo@g.com",
            "gender": "M",
            "birth": "2000-12-12T06:55:00Z",
            "level": "SR",
            "password": "Pablo",
            "is_staff": True
        }
        cls.id_user = client.post('/users/', user_data, format='json').json()['id']
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

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        self.all_articles = []
        for i in range(0, 5):
            article_json = {
                'title': "Title example " + str(i),
                'text': 'Text example'
            }
            response = self.client.post('/articles/', article_json, format='json')
            self.all_articles.append(response.json())

    def test_edit_one_article(self):
        article = self.all_articles[0]
        new_article_json = {
            'title': "New title example",
            'text': 'New text example'
        }
        response = self.client.put(f'/articles/{article["id"]}/', new_article_json)

        for field in new_article_json:
            self.assertEqual(response.json()[field], new_article_json[field])

    def test_try_edit_one_user_no_body(self):
        article = self.all_articles[0]
        new_article_json = {}
        response = self.client.put(f'/articles/{article["id"]}/', new_article_json)

        self.assertEqual(response.json(), {'title': ['This field is required.'], 'text': ['This field is required.']})
        self.assertEqual(response.status_code, 400)

    def test_try_edit_one_article_repeated_title(self):
        article_1 = self.all_articles[0]
        article_2 = self.all_articles[1]
        new_article_json = {
            'title': article_2['title'],
            'text': 'New text example'
        }
        response = self.client.put(f'/articles/{article_1["id"]}/', new_article_json)

        self.assertEqual(response.json(), {'title': ['article with this title already exists.']})
        self.assertEqual(response.status_code, 400)

    def test_try_edit_one_article_bad_id(self):
        new_article_json = {
            'title': 'New title example',
            'text': 'New text example'
        }
        response = self.client.put('/articles/bad_id/', new_article_json)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'detail': 'Not found.'})

    def test_try_edit_one_article_no_credentials(self):
        # in setUp credentials were setted, so now we have to remove them.
        self.client.credentials(HTTP_AUTHORIZATION='BAD TOKEN')

        article = self.all_articles[0]
        new_article_json = {
            'title': "New title example",
            'text': 'New text example'
        }
        response = self.client.put(f'/articles/{article["id"]}/', new_article_json)

        self.assertEqual('Authentication credentials were not provided.', response.json()['detail'])
        self.assertEqual(401, response.status_code)


# python manage.py test app_articles.tests.tests_articles.DeleteOneArticleTestCase
class DeleteOneArticleTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        client = APIClient()
        user_data = {
            "username": "Pablo",
            "email": "Pablo@g.com",
            "gender": "M",
            "birth": "2000-12-12T06:55:00Z",
            "level": "SR",
            "password": "Pablo",
            "is_staff": True
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

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        self.all_articles = []
        for i in range(0, 5):
            article_json = {
                'title': "Title example " + str(i),
                'text': 'Text example'
            }
            response = self.client.post('/articles/', article_json, format='json')
            self.all_articles.append(response.json())

    def test_delete_one_user(self):
        response = self.client.delete(f'/articles/{self.all_articles[0]["id"]}/')
        self.assertEqual(204, response.status_code)

    def test_try_delete_one_user_twice(self):
        response_1 = self.client.delete(f'/articles/{self.all_articles[0]["id"]}/')
        response_2 = self.client.delete(f'/articles/{self.all_articles[0]["id"]}/')
        self.assertEqual(204, response_1.status_code)
        self.assertEqual(404, response_2.status_code)

    def test_try_delete_non_existent_user(self):
        response = self.client.delete('/users/NON-EXISTENT-ID/')
        self.assertEqual(404, response.status_code)

    def test_try_delete_an_article_no_token(self):
        # in setUp credentials were setted, so now we have to remove them.
        self.client.credentials(HTTP_AUTHORIZATION='BAD TOKEN')

        response = self.client.delete(f'/articles/{self.all_articles[0]["id"]}/')
        self.assertEqual(401, response.status_code)


# python manage.py test app_articles.tests.tests_articles.PartialModifyOneArticleTestCase
class PartialModifyOneArticleTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        client = APIClient()
        user_data = {
            "username": "Pablo",
            "email": "Pablo@g.com",
            "gender": "M",
            "birth": "2000-12-12T06:55:00Z",
            "level": "SR",
            "password": "Pablo",
            "is_staff": True
        }
        cls.id_user = client.post('/users/', user_data, format='json').json()['id']
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

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        self.all_articles = []
        for i in range(0, 5):
            article_json = {
                'title': "Title example " + str(i),
                'text': 'Text example'
            }
            response = self.client.post('/articles/', article_json, format='json')
            self.all_articles.append(response.json())

    def test_partial_modify_one_article(self):
        article = self.all_articles[0]
        update_field = {
            'text': 'New text patch'
        }
        response = self.client.patch(f'/articles/{article["id"]}/', update_field, format='json')

        self.assertEqual(200, response.status_code)
        self.assertEqual(update_field['text'], response.json()['text'])

    def test_try_partial_modify_an_article_unique_field_already_used(self):
        article_1 = self.all_articles[0]
        article_2 = self.all_articles[1]
        update_field = {
            'title': article_2['title']
        }
        response = self.client.patch(f'/articles/{article_1["id"]}/', update_field, format='json')

        self.assertEqual(400, response.status_code)
        self.assertEqual(response.json(), {'title': ['article with this title already exists.']})

    def test_try_partial_modify_non_existent_user(self):
        response = self.client.patch('/users/NON-EXISTENT-ID/', {})
        self.assertEqual(404, response.status_code)
