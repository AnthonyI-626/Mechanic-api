from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import  mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from datetime import date
from app.extensions import ma, db, Base


class Mechanic(Base):
    __tablename__ = 'customers'
    
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(db.String(250), nullable = False)
    email: Mapped[str] = mapped_column(db.String(360), nullable = False, unique = True)
    phone: Mapped[str] = mapped_column(db.String(10), nullable = False, unique = True)
    DOB: Mapped[date] 
    password: Mapped[str] = mapped_column(db.String(250), nullable = False)
    
    service_tickets = relationship('ServiceTicket', back_populates='mechanic')

    
    
class ServiceTicket(Base):
    __tablename__ = 'service_tickets'
    
    id: Mapped[int] = mapped_column(primary_key = True)
    description: Mapped[str] = mapped_column(db.String(500), nullable = False)
    date_created: Mapped[date] = mapped_column(db.Date)
    status: Mapped[str] = mapped_column(db.String(50), nullable = False) 
    
    mechanic_id: Mapped[int] = mapped_column(ForeignKey('customers.id'), nullable = False)
    mechanic: Mapped['Mechanic'] = relationship(back_populates='service_tickets')
    
      


