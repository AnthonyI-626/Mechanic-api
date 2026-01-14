from app.extensions import ma
from app.models import Customers


class CustomerSchema(ma.Schema):
    class Meta:
        model = Customers
        load_instance = True
        fields = ('id', 'name', 'email', 'password', 'phone', 'DOB')
        
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)


login_schema = CustomerSchema(only=('email', 'password'))