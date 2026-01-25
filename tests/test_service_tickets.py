import unittest
from app import create_app
from app.models import db, ServiceTicket, Mechanic, Inventory, Customers
from datetime import date


class TestServiceTickets(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        db.drop_all()
        db.create_all()


        self.customer = Customers(
            name="Test User",
            email="test@user.com",
            phone="1234567899",
            DOB=date(1990, 1, 1),
            password="testpass"
        )
        db.session.add(self.customer)

        
        self.mechanic = Mechanic(
            name="Test Mechanic",
            email="mech@test.com",
            phone="1112223333",
            DOB=date(1985, 5, 5),
            password="mechpass"
        )
        db.session.add(self.mechanic)

      
        self.part = Inventory(
            name="Brake Pad",
            quantity=10,
            price=49.99
        )
        db.session.add(self.part)

        db.session.commit()

        
        self.ticket = ServiceTicket(
            description="Oil change",
            status="open",
            customer_id=self.customer.id
        )
        db.session.add(self.ticket)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

 
    def test_create_service_ticket(self):
        payload = {
            "description": "Flat tire repair",
            "status": "open",
            "customer_id": self.customer.id
        }

        response = self.client.post("/service_tickets/", json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["description"], "Flat tire repair")

    def test_invalid_service_ticket_creation(self):
        payload = {
            "status": "open"
        }

        response = self.client.post("/service_tickets/", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("description", response.json["error"])

    def test_get_service_tickets(self):
        response = self.client.get("/service_tickets/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreaterEqual(len(response.json), 1)


    def test_get_service_ticket(self):
        response = self.client.get(f"/service_tickets/{self.ticket.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["description"], "Oil change")

    
    def test_update_service_ticket(self):
        payload = {
            "status": "closed"
        }

        response = self.client.put(
            f"/service_tickets/{self.ticket.id}",
            json=payload
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "closed")

   
    def test_assign_mechanic(self):
        payload = {
            "mechanic_id": self.mechanic.id
        }

        response = self.client.put(
            f"/service_tickets/{self.ticket.id}/mechanic",
            json=payload
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["mechanic"]["id"], self.mechanic.id)

 
    def test_update_ticket_parts(self):
        payload = {
            "add_ids": [self.part.id]
        }

        response = self.client.put(
            f"/service_tickets/{self.ticket.id}/parts",
            json=payload
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["parts"]), 1)

    
    def test_my_tickets(self):
       
        login_payload = {
            "email": self.customer.email,
            "password": "testpass"
        }

        login_response = self.client.post("/customers/login", json=login_payload)
        token = login_response.json["token"]

        response = self.client.get(
            "/service_tickets/my-tickets",
            headers={"Authorization": f"Bearer {token}"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json), 1)
