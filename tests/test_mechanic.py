import unittest
from app import create_app
from app.models import db, Mechanic
from datetime import datetime


class TestMechanic(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        db.drop_all()
        db.create_all()

       
        self.mechanic = Mechanic(
            name="Test Mechanic",
            email="mech@test.com",
            phone="1112223333",
            DOB=datetime(1990, 1, 1),
            password="testpass"
        )
        db.session.add(self.mechanic)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

 
    def test_create_mechanic(self):
        payload = {
            "name": "John Doe",
            "email": "john@shop.com",
            "phone": "9998887777",
            "DOB": "1985-05-05",
            "password": "securepass"
        }

        response = self.client.post("/mechanics/", json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["name"], "John Doe")

   
    def test_invalid_mechanic_creation(self):
        payload = {
            "name": "Bad Mechanic",
            "phone": "5554443333",
            "password": "nopemail"
        }

        response = self.client.post("/mechanics/", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.json["error"])

    def test_get_mechanics(self):
        response = self.client.get("/mechanics/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreaterEqual(len(response.json), 1)

    
    def test_get_mechanic(self):
        response = self.client.get(f"/mechanics/{self.mechanic.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["email"], "mech@test.com")

    def test_update_mechanic(self):
        payload = {
            "name": "Updated Name",
            "email": "mech@test.com",
            "phone": "1112223333",
            "DOB": "1990-01-01",
            "password": "testpass"
        }

        response = self.client.put(
            f"/mechanics/{self.mechanic.id}",
            json=payload
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "Updated Name")

    def test_delete_mechanic(self):
        response = self.client.delete(f"/mechanics/{self.mechanic.id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("successfully deleted", response.json["message"])

 
    def test_most_active_mechanics(self):
        response = self.client.get("/mechanics/most-active")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

