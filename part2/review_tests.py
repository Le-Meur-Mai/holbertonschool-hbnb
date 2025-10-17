import unittest
from app import create_app
from app.services import facade


class TestReviewEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        self.user = facade.create_user({
            "first_name": "Test",
            "last_name": "User",
            "email": "test@gmail.com"
        })

        # Create a test place
        self.place = facade.create_place({
            "title": "Test Place",
            "description": "A test description",
            "price": 0.0,
            "latitude": 0.0,
            "longitude": 0.0,
            "owner_id": self.user.id
        })

    def test_create_review_success(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Even the fridge is more efficiently than my backend.",
            "rating": 5,
            "user_id": self.user.id,
            "place_id": self.place.id
        })
        self.assertEqual(response.status_code, 201)

    def test_create_review_invalid_text(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 5,
            "user_id": self.user.id,
            "place_id": self.place.id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_rating(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Would respawn here again.",
            "rating": 9,
            "user_id": self.user.id,
            "place_id": self.place.id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_user(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "I came to rest, but ended up optimizing my life.",
            "rating": 5,
            "user_id": "user_id",
            "place_id": self.place.id
        })
        self.assertEqual(response.status_code, 404)

    def test_create_review_invalid_place(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "The cat is clearly the sysadmin of the house.",
            "rating": 5,
            "user_id": self.user.id,
            "place_id": "place_id"
        })
        self.assertEqual(response.status_code, 404)

    def test_get_all_reviews(self):
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)

    def test_get_review_by_id(self):
        # Create review first
        review = facade.create_review({
            "text": "Review",
            "rating": 4,
            "user_id": self.user.id,
            "place_id": self.place.id
        })

        response = self.client.get(f'/api/v1/reviews/{review.id}')
        self.assertEqual(response.status_code, 200)

    def test_get_review_not_found(self):
        response = self.client.get('/api/v1/reviews/review-id')
        self.assertEqual(response.status_code, 404)

    def test_update_review_success(self):
        review = facade.create_review({
            "text": "The fridge is clearly a house-elf in disguise.",
            "rating": 3,
            "user_id": self.user.id,
            "place_id": self.place.id
        })

        response = self.client.put(f'/api/v1/reviews/{review.id}', json={
            "text": "If I could, I'd set up a permanent Portkey here.",
            "rating": 5,
            "user_id": self.user.id,
            "place_id": self.place.id
        })
        self.assertEqual(response.status_code, 200)

    def test_update_review_not_found(self):
        response = self.client.put('/api/v1/reviews/fake-id', json={
            "text": "Absolute silence. It's magic or the portraits are asleep",
            "rating": 5,
            "user_id": self.user.id,
            "place_id": self.place.id
        })
        self.assertEqual(response.status_code, 404)

    def test_update_review_invalid_rating(self):
        review = facade.create_review({
            "text": "The bedding? I'd swear it was woven by Aragog himself",
            "rating": 3,
            "user_id": self.user.id,
            "place_id": self.place.id
        })
        response = self.client.put(f'/api/v1/reviews/{review.id}', json={
            "text": "I slept so well thought I taken Pillow Polyjuice Potion.",
            "rating": 10,
            "user_id": self.user.id,
            "place_id": self.place.id
        })
        self.assertEqual(response.status_code, 400)

    def test_delete_review_success(self):
        review = facade.create_review({
            "text": "Feels like the Burrow's fireplace lives here.",
            "rating": 3,
            "user_id": self.user.id,
            "place_id": self.place.id
        })
        response = self.client.delete(f'/api/v1/reviews/{review.id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_review_not_found(self):
        response = self.client.delete('/api/v1/reviews/fake-id')
        self.assertEqual(response.status_code, 404)

    def test_get_reviews_by_place(self):
        facade.create_review({
            "text": "It’s basically the Room of Requirement.",
            "rating": 4,
            "user_id": self.user.id,
            "place_id": self.place.id
        })
        response = self.client.get(
                        f'/api/v1/reviews/places/{self.place.id}/reviews')
        self.assertEqual(response.status_code, 200)

    def test_get_reviews_by_place_place_not_found(self):
        response = self.client.get('/api/v1/reviews/places/fake-id/reviews')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
