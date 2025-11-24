from flask import Flask, render_template, request, redirect
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
import requests

jwt = JWTManager()

bcrypt = Bcrypt()

db = SQLAlchemy()


def create_app(config_class="config.DevelopmentConfig"):
    """Create and configure the Flask application with Flask-RESTX.

    This function initializes the Flask app, sets up the RESTX API,
    and registers all namespaces for version 1 of the HBnB API.

    Returns:
        Flask: The configured Flask application instance.
    """
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.auth import api as auth_ns

    app = Flask(__name__)
    app.config.from_object(config_class)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Initialize Flask-RESTX API with documentation
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/',
        prefix='/api/v1'
    )
    '''Add a prefix to initialize namespaces and the welcome page of api to
    /api/v1 instead of just /, so when toy start the app, the user is directed
    on the index page'''

    db.init_app(app)

    # Register the users namespace
    api.add_namespace(users_ns, path='/users')
    # Register the places namespace
    api.add_namespace(places_ns, path='/places')
    # Register the amenities namespace
    api.add_namespace(amenities_ns, path='/amenities')
    # Register the reviews namespace
    api.add_namespace(reviews_ns, path='/reviews')
    # Register the authentification namespace
    api.add_namespace(auth_ns, path='/auth')

    @app.route('/')
    def index():
        return redirect('/index')

    @app.route('/index')
    def home():
        return render_template('index.html')

    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/place')
    def places():
        try:
            id = request.args.get('id')
            if id == "":
                id = 1
            # If the ID is Null, it won't crash

            place = requests.get(f'http://127.0.0.1:5000/api/v1/places/{id}')
            place = place.json()
            reviews = requests.get(
                f'http://127.0.0.1:5000/api/v1/reviews/places/{id}/reviews')
            reviews = reviews.json()
        except Exception as error:
            place = None
            reviews = None
        if place.get('error'):
            place = None
            reviews = None
        return render_template('place.html', place=place, reviews=reviews)

    @app.route('/review')
    def review():
        try:
            id = request.args.get('id')
            if id == "":
                id = 1
            # If the ID is Null, it won't crash

            place = requests.get(f'http://127.0.0.1:5000/api/v1/places/{id}')
            place = place.json()
        except Exception:
            place = None
        if place.get('error'):
            place = None

        return render_template('add_review.html', place=place)

    return app
