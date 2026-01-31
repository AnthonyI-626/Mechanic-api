from app.models import ServiceTicket, Mechanic, Inventory
from app.extensions import ma


class MechanicNestedSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        fields = ("id", "name", "email", "phone")


class InventoryNestedSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        fields = ("id", "name", "price")


class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    mechanic = ma.Nested(MechanicNestedSchema)
    parts = ma.List(ma.Nested(InventoryNestedSchema))

    class Meta:
        model = ServiceTicket
        include_fk = True
        load_instance = True


service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
