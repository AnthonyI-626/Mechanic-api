from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import  mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from datetime import date
from app.extensions import ma, db, Base









class Mechanic(Base):
    __tablename__ = 'mechanics'
    
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(db.String(250), nullable = False)
    email: Mapped[str] = mapped_column(db.String(360), nullable = False, unique = True)
    phone: Mapped[str] = mapped_column(db.String(10), nullable = False, unique = True)
    DOB: Mapped[date] 
    password: Mapped[str] = mapped_column(db.String(250), nullable = False)
    
    cars: Mapped[list['Car']] = relationship(back_populates='mechanic')
    
class Car(Base):
    __tablename__ = 'cars'
    
    id: Mapped[int] = mapped_column(primary_key = True)
    make: Mapped[str] = mapped_column(db.String(250), nullable = False)
    model: Mapped[str] = mapped_column(db.String(250), nullable = False)
    year: Mapped[int] = mapped_column(db.Integer, nullable = False)
    vin: Mapped[str] = mapped_column(db.String(17), nullable = False, unique = True)
    
    customer_id: Mapped[int] = mapped_column(ForeignKey('mechanics.id'))
    mechanic: Mapped['Mechanic'] = relationship(back_populates="cars")
    
    

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        
customer_schema = MechanicSchema()