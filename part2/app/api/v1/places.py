from flask_restx import Namespace, Resource, fields
from app.services import facade

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
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})




@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):

        """Register a new place"""

        place_data = api.payload

        existing_place = facade.get_place_by_localisation(place_data['latitude'], place_data['longitude'])
        if existing_place is True:
            return {'error': 'This place already exists'}, 400
        existing_user = facade.get_user(place_data['owner_id'])
        if not existing_user:
            return {'error': 'This user doesn\'t exist'}, 404
        new_place = facade.create_place(place_data)
        return { 'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner_id': new_place.owner_id}, 201
        
    """Retrieve a list of all places"""

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        places = facade.get_all_places()
        place_list = [{
            'id' : place.id,
            'title' : place.title,
            'latitude' : place.latitude,
            'longitude' : place.longitude,
        } for place in places]

        return place_list, 200



    
    
"""Get place details by ID"""

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        list_amenities = []
        if len(place.amenities) > 0:
            list_amenities = [{
                'id': amenity.id,
                'name': amenity.name
            }for amenity in place.amenities]
                
        data_owner = facade.get_user(place.owner_id)
        return { 'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner': {"id": place.owner_id,
                          "first_name": data_owner.first_name,
                          "last_name": data_owner.last_name,
                          "email": data_owner.email},
                'amenities': list_amenities}, 200
        
    """Adding an amenity to a place"""

    @api.response(404, 'Place not found')
    @api.response(200, 'Amenity added successfuly')
    def post(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        data_amenity = api.payload

        amenity = facade.get_amenity(data_amenity["id"])
        place.amenities.append(amenity)
        return {'amenity successfully added': {"id": amenity.id,
                                               'name': amenity.name}}, 200


    """Update a place's information"""

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        data_place = api.payload
        facade.update_place(place_id, data_place)
        return {"message": "Place updated successfully"}, 200
