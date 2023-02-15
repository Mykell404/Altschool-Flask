import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from ..models.orders import Order
from flask_jwt_extended import create_access_token


class OrderTestCase(unittest.TestCase):
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

    def test_get_all_orders(self):
        token = create_access_token(identity='testuser')
        headers = {
            'Authorization': f"Bearer {token}"
        }
        response = self.client.get('/orders/orders', headers=headers)

        assert response.status_code == 200

        assert response.json == []

    def test_create_order(self):
        token = create_access_token(identity='testuser')
        headers = {
            'Authorization': f"Bearer {token}"
        }

        data = {
            "size": "SMALL",
            "quantity": 2,
            "flavour": "Apple",
            "order_status": "PENDING"
        }

        response = self.client.post(
            'orders/orders', headers=headers, json=data)

        assert response.status_code == 201
