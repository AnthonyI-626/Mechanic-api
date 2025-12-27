from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from datetime import date
from flask import current_app as app
from app.extensions import ma



class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


db.init_app(app)


class Customer(Base):
    __tablename__ = 'customers'
    
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(db.String(250), nullable = False)
    email: Mapped[str] = mapped_column(db.String(360), nullable = False, unique = True)
    phone: Mapped[str] = mapped_column(db.String(10), nullable = False, unique = True)
    DOB: Mapped[date] 
    password: Mapped[str] = mapped_column(db.String(250), nullable = False)
    
    cars: Mapped[list['Car']] = relationship(back_populates='customer')
    
class Car(Base):
    __tablename__ = 'cars'
    
    id: Mapped[int] = mapped_column(primary_key = True)
    make: Mapped[str] = mapped_column(db.String(250), nullable = False)
    model: Mapped[str] = mapped_column(db.String(250), nullable = False)
    year: Mapped[int] = mapped_column(db.Integer, nullable = False)
    vin: Mapped[str] = mapped_column(db.String(17), nullable = False, unique = True)
    
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id'))
    customer: Mapped['Customer'] = relationship(back_populates="cars")
    
    

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        
customer_schema = CustomerSchema()