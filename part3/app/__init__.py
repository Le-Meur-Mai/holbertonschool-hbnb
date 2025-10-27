from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns


def create_app():
    """Create and configure the Flask application with Flask-RESTX.

    This function initializes the Flask app, sets up the RESTX API,
    and registers all namespaces for version 1 of the HBnB API.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)

    # Initialize Flask-RESTX API with documentation
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/'
    )

    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')
    # Register the places namespace
    api.add_namespace(places_ns, path='/api/v1/places')
    # Register the amenities namespace
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    # Register the reviews namespace
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return app
