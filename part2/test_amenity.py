import unittest
from app import create_app
from app.models.amenity import Amenity


class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_amenity(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Wi-Fi"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_empty_amenity(self):
        self.client.post('/api/v1/amenities/', json={
            "name": ""
        })
        self.assertRaises(ValueError)

    def test_create_same_amenity(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Wi-Fi"
        })
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Wi-Fi"
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_amenities(self):
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)

    def test_valid_update_amenity(self):
        new_amenity = Amenity("Wi-Fi")
        new_amenity.update({"name": "Jacuzzi"})
        self.assertEqual(new_amenity.name, "Jacuzzi")

    def test_invalid_update_amenity(self):
        new_amenity = Amenity("Wi-Fi")
        with self.assertRaises(ValueError):
            new_amenity.update({"name": ""})


if __name__ == '__main__':
    unittest.main()
