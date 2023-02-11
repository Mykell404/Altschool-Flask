import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from werkzeug.security import generate_password_hash
from ..models.users import User


class UserTestCase(unittest.TestCase):
    def setUp(self):
        # Set up a test instance of create_app
        self.app = create_app(config=config_dict['test'])

        # Set up the app context
        self.appctx = self.app.app_context()

        # Create the app context
        self.appctx.push()

        # Create the test client
        self.client = self.app.test_client()

        db.create_all()

    def tearDown(self):
        db.drop_all()

        self.appctx.pop()

        self.app = None

        self.client = None

    def test_user_registration(self):
        """
        Test user registrations
        """
        data = {
            "username": "test user",
            "email": "testt@gmail.com",
            "password": "password"
        }
        response = self.client.post('/auth/signup', json=data)

        user = User.query.filter_by(email='testt@gmail.com').first()

        assert user.username == 'test user'

        assert response.status_code == 201

    def test_user_login(self):
        """Test user login"""

        data = {
            "email": "testt@gmail.com",
            "password": "password"
        }
        response = self.client.post('/auth/login', json=data)

        assert response.status_code == 200
