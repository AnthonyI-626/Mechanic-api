Mechanic API — Service Ticket Management System
A lightweight RESTful API built with Flask, SQLAlchemy 2.0, and MySQL, designed to manage mechanics and service tickets. 
This project demonstrates clean API design, relational modeling, Marshmallow validation, and end‑to‑end testing using Postman.

🚀 Features

Mechanics
Create a mechanic

Retrieve all mechanics

Retrieve a single mechanic

Assign a mechanic to a service ticket

Remove a mechanic from a service ticket

Service Tickets
Create a service ticket

Retrieve all tickets

Retrieve a single ticket

Assign/remove mechanics

One‑to‑many relationship (each ticket has one mechanic)

Tech Stack
Flask (Blueprints, routing)

SQLAlchemy 2.0 ORM

MySQL (via PyMySQL)

Marshmallow (schema validation + serialization)

Postman (E2E testing)

📦 Project Structure

Mechanic-api/
│
├── app/
│   ├── blueprints/
│   │   ├── Mechanic/
│   │   │   ├── routes.py
│   │   │   └── schemas.py
│   │   ├── ServiceTicket/
│   │   │   ├── routes.py
│   │   │   └── schemas.py
│   │
│   ├── models/
│   │   ├── mechanic.py
│   │   └── service_ticket.py
│   │
│   ├── config.py
│   └── __init__.py
│
├── Requirements.txt
└── README.md

⚙️ Setup Instructions

1. Clone the Repository
bash
git clone <your-repo-url>
cd Mechanic-api
2. Create and Activate a Virtual Environment
bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
3. Install Dependencies
bash
pip install -r Requirements.txt
4. Configure Environment Variables
Create a .env file or update config.py with your MySQL credentials:

Code
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=mechanic_api
5. Create the Database
In MySQL Workbench:

sql
CREATE DATABASE mechanic_api;
6. Run the Application
bash
flask run
The API will be available at:

Code
http://localhost:5000
🗄️ Database Model Overview
Mechanic
Field	Type	Notes
id	int	PK
name	string	required
email	string	unique
phone	string	required
DOB	date	required
password	string	required
ServiceTicket
Field	Type	Notes
id	int	PK
description	string	required
date_created	date	required
status	string	required
mechanic_id	int	FK → mechanics.id (nullable or not depending on your design)
🔌 API Endpoints

Mechanics
Method	Endpoint	Description
POST	/mechanics/	Create a mechanic
GET	/mechanics/	Get all mechanics
GET	/mechanics/	Get a mechanic by ID
Service Tickets
Method	Endpoint	Description
POST	/service_tickets/	Create a service ticket
GET	/service_tickets/	Get all tickets
GET	/service_tickets/	Get a ticket by ID
PUT	/service_tickets//assign-mechanic/	Assign mechanic
PUT	/service_tickets//remove-mechanic/	Remove mechanic
