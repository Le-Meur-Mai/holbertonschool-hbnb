from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True,
                           description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True,
                          description='Price per night'),
    'latitude': fields.Float(required=True,
                             description='Latitude of the place'),
    'longitude': fields.Float(required=True,
                              description='Longitude of the place'),
    'owner_id': fields.String(required=True,
                              description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True,
                             description="List of amenities ID's")
})


@api.route('/')
class PlaceList(Resource):
    """Resource for creating and listing places."""

    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """
        Register a new place.

        This endpoint allows clients to register a new place by providing
        its title, description, location (latitude, longitude), price,
        owner ID, and a list of amenity IDs.

        Returns:
            list: A JSON response containing the created place's details
            and a 201 status code upon success.
            If the place already exists (same coordinates),
                returns a 400 error.
            If the specified owner does not exist, returns a 404 error.
            If the input data is invalid, returns a 400 error.
        """

        place_data = api.payload

        existing_place = facade.get_place_by_localisation(
            place_data['latitude'],
            place_data['longitude'])
        if existing_place is True:
            return {'error': 'This place already exists'}, 400
        existing_user = facade.get_user(place_data['owner_id'])
        if not existing_user:
            return {'error': 'This user doesn\'t exist'}, 404
        current_user = get_jwt_identity()
        if current_user != place_data['owner_id']:
            return {'error': 'The owner\'s id is not yours'},404
        try:
            new_place = facade.create_place(place_data)
        except (ValueError, TypeError):
            return {'error': 'Invalid input data'}, 400

        return {'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner_id': new_place.owner_id}, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """
        Retrieve a list of all registered places.

        Returns:
            list: A JSON list of all places, each including their ID, title,
            latitude, and longitude, along with a 200 status code.
        """
        places = facade.get_all_places()
        place_list = [{
            'id': place.id,
            'title': place.title,
            'latitude': place.latitude,
            'longitude': place.longitude,
        } for place in places]

        return place_list, 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    """Resource for retrieving, updating, or modifying a specific place."""

    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Retrieve detailed information about a specific place.

        Args:
            place_id (str): The unique identifier of the place.

        Returns:
            list: A JSON object containing full details of the place,
            including owner information and amenities,
                along with a 200 status code.
            If the place is not found, returns a 404 error.
        """
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        list_amenities = []
        if len(place.amenities) > 0:
            list_amenities = [{
                'id': amenity.id,
                'name': amenity.name
            } for amenity in place.amenities]

        data_owner = facade.get_user(place.owner_id)
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {
                "id": place.owner_id,
                "first_name": data_owner.first_name,
                "last_name": data_owner.last_name,
                "email": data_owner.email
            },
            'amenities': list_amenities
        }, 200

    @api.response(404, 'Place not found')
    @api.response(200, 'Amenity added successfuly')
    def post(self, place_id):
        """
        Add an amenity to a specific place.

        This endpoint allows adding an existing amenity to a place.

        Args:
            place_id (str): The unique identifier of the place.

        Returns:
            list: A JSON object confirming the addition of the amenity
            with a 200 status code.
            If the place is not found, returns a 404 error.
        """
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        data_amenity = api.payload
        amenity = facade.get_amenity(data_amenity["id"])
        place.amenities.append(amenity)
        return {
            'amenity successfully added': {
                "id": amenity.id,
                'name': amenity.name
            }
        }, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """
        Update an existing place.

        This endpoint allows modifying details of an existing place,
        such as title, description, location, price, owner, or amenities.

        Args:
            place_id (str): The unique identifier of the place to update.

        Returns:
            list: A success message with a 200 status code upon success.
            If the place is not found, returns a 404 error.
            If the input data is invalid, returns a 400 error.
        """
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        data_place = api.payload
        existing_user = facade.get_user(data_place['owner_id'])
        if not existing_user:
            return {'error': 'This user doesn\'t exist'}, 404
        try:
            facade.update_place(place_id, data_place)
        except ValueError:
            return {'error': 'Invalid input data'}, 400

        return {"message": "Place updated successfully"}, 200
