from app import create_app
from app.models import db, Customers
from app.utils.util import encode_token
import unittest

class TestCustomer(unittest.TestCase):

    def setUp(self):
        self.app = create_app('TestingConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        db.drop_all()
        db.create_all()

        self.customer = Customers(
            name="test_user",
            email="test@email.com",
            phone="1234567899",
            password='test'
        )
        db.session.add(self.customer)
        db.session.commit()

        self.token = encode_token(self.customer.id, self.app.config["SECRET_KEY"])


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

        
    def test_create_customer(self):
        customers_payload = {
            "name": "John Doe",
            "email": "jd@email.com",
            "phone": "1234566666",
            "password": "123"
        }

        response = self.client.post('/customers/', json=customers_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "John Doe")
        
    def test_invalid_creation(self):
        customer_payload = {
            "name": "John Doe",
            "phone": "123-456-7890",
            "password": "123"       
        }

        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error']['email'], ['Missing data for required field.'])
        
    def test_login_customer(self):
        credentials = {
            "email": "test@email.com",
            "password": "test"
        }

        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        return response.json['token']
    
    def test_update_customer(self):
        update_payload = {
            "name": "Peter",
            "phone": "1234567890",
            "email": "test@email.com",
            "password": "test"
        }

        headers = {'Authorization': "Bearer " + self.test_login_customer()}

        response = self.client.put(f'/customers/{self.customer.id}', json=update_payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Peter')
        self.assertEqual(response.json['email'], 'test@email.com')
