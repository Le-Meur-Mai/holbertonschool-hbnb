import unittest
from app import create_app

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Light",
            "last_name": "Yagami",
            "email": "light.yagami@gmail.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Saitama",
            "last_name": "",
            "email": "saitama@gmail.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_duplicate_email(self):
        self.client.post('/api/v1/users/', json={
            "first_name": "Son",
            "last_name": "Goku",
            "email": "sayan@gmail.com"
        })
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Son",
            "last_name": "Gohan",
            "email": "sayan@gmail.com"
        })
        self.assertEqual(response.status_code, 400)
