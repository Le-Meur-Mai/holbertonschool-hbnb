from app.models.basemodel import BaseModel as BaseModel
from email_validator import validate_email, EmailNotValidError
from app import bcrypt, db
import uuid
from sqlalchemy.orm import validates


class User(BaseModel):
    """Model representing a user in the system.

    Inherits from BaseModel and adds attributes for the user's name,
    email, admin status, and associated reviews and places.

    Attributes:
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        email (str): Email address of the user.
        is_admin (bool): Whether the user has admin privileges.
        reviews (list): List of Review objects created by the user.
        places (list): List of Place objects owned by the user.
    """

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, email, password):
        """Initialize a new User instance with validation."""
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.hash_password(password)
        self.is_admin = False
        self.reviews = []
        self.places = []


    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        return self.password

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    @validates("email")
    def verify_email(self, key, value):
        """Set the user's email address with validation.

        Args:
            value (str): Email address.

        Raises:
            ValueError: If the email is empty or has invalid format.
        """
        if len(value) > 120:
            raise ValueError("Email adress too long")
        try:
            valid = validate_email(value)
            email = valid.normalized
        except EmailNotValidError:
            raise ValueError("Invalid email address format")

        return email

    @validates("first_name")
    def verify_first_name(self, key, value):
        """Verify the user's first name.

        Args:
            value (str): First name.

        Raises:
            ValueError: If the first name is empty or None.
        """
        if not value or type(value) != str or len(value) > 50:
            raise ValueError
        return value


    @validates("last_name")
    def verify_last_name(self, key, value):
        """Verify the user's last name.

        Args:
            value (str): Last name.

        Raises:
            ValueError: If the last name is empty or None.
        """
        if not value or type(value) != str or len(value) > 50:
            raise ValueError
        return value

    def add_review(self, review):
        """Add a review to the user.

        Args:
            review: A Review object to associate with this user.
        """
        self.reviews.append(review)

    def add_place(self, place):
        """Add a place to the user.

        Args:
            place: A Place object to associate with this user.
        """
        self.places.append(place)
