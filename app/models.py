
from sqlalchemy.orm import  mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from datetime import date
from app.extensions import db, Base


class Mechanic(Base):
    __tablename__ = 'mechanics'
    
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(db.String(250), nullable = False)
    email: Mapped[str] = mapped_column(db.String(360), nullable = False, unique = True)
    phone: Mapped[str] = mapped_column(db.String(10), nullable = False, unique = True)
    DOB: Mapped[date] 
    password: Mapped[str] = mapped_column(db.String(250), nullable = False)
    
    tickets = relationship('ServiceTicket', back_populates='mechanic')

class Customers(Base):
    __tablename__ = 'customers'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(250), nullable=False)
    email: Mapped[str] = mapped_column(db.String(255),unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)
    phone: Mapped[str] = mapped_column(db.String(15), unique=True, nullable=False)
    DOB: Mapped[str] = mapped_column(db.String(20), nullable=True)
    
    tickets = relationship("ServiceTicket", back_populates="customer")

    
ticket_parts = db.Table( 'ticket_parts', db.Column(
    'ticket_id', db.Integer, db.ForeignKey('service_tickets.id'), primary_key=True),
    db.Column('inventory_id', db.Integer, db.ForeignKey('inventory.id'), primary_key=True))
    
    
class ServiceTicket(Base):
    __tablename__ = 'service_tickets'
    
    id: Mapped[int] = mapped_column(primary_key=True)

    customer_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('customers.id'), nullable=False)
    mechanic_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('mechanics.id'), nullable=False)

    description: Mapped[str] = mapped_column(db.String(500), nullable=False)
    status: Mapped[str] = mapped_column(db.String(50), nullable=False)
    date_created: Mapped[date] = mapped_column(db.Date, default=date.today)

    customer = relationship("Customers", back_populates="tickets")
    mechanic = relationship("Mechanic", back_populates="tickets")

    parts = db.relationship('Inventory', secondary='ticket_parts', back_populates='tickets')

     
    
class Inventory(Base):
    __tablename__ = 'inventory'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(250), nullable=False)
    price: Mapped[float] = mapped_column(db.Float, nullable=False)
    quantity: Mapped[int] = mapped_column(db.Integer, nullable=False)

    
    tickets = db.relationship('ServiceTicket', secondary='ticket_parts', back_populates='parts')
   
    



