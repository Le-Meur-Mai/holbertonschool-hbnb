import unittest
from app import create_app
from app.models.user import User

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_valid_user_creation(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Light",
            "last_name": "Yagami",
            "email": "light.yagami@mail.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_invalid_empty_last_name(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Saitama",
            "last_name": "",
            "email": "saitama@mail.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_invalid_empty_first_name(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "Albator",
            "email": "albator@mail.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_invalid_empty_email(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Tanjiro",
            "last_name": "Kamado",
            "email": ""
        })
        self.assertEqual(response.status_code, 400)

    def test_invalid_duplicate_email(self):
        self.client.post('/api/v1/users/', json={
            "first_name": "Son",
            "last_name": "Goku",
            "email": "sayan@mail.com"
        })
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Son",
            "last_name": "Gohan",
            "email": "sayan@mail.com"
        })
        self.assertEqual(response.status_code, 400)
    
    def test_update_valid_fields(self):
        user = User(first_name="Yugi", last_name="Yami", email="yugi.yami@mail.com")
        user.update({
            "first_name": "Yugi",
            "last_name": "Muto",
            "email": "yugi.muto@mail.com"
        })
        self.assertEqual(user.first_name, "Yugi")
        self.assertEqual(user.last_name, "Muto")
        self.assertEqual(user.email, "yugi.muto@mail.com")

    def test_update_invalid_first_name(self):
        user = User(first_name="Naruto", last_name="Uzumaki", email="naruto.uzumaki@mail.com")
        with self.assertRaises(ValueError):
            user.update({"first_name": ""})
    
    def test_update_invalid_last_name(self):
        user = User(first_name="Gojo", last_name="Satoru", email="gojo.satoru@mail.com")
        with self.assertRaises(ValueError):
            user.update({"last_name": ""})

if __name__ == '__main__':
    unittest.main()
