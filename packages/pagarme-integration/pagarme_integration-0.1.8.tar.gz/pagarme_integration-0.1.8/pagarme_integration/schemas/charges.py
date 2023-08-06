from pagarme_integration.schemas.transactions import TransactionSchema
from pagarme_integration.schemas.customers import CustomerSchema


class ChargeSchema:
    __get = {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "gateway_id": {"type": "string"},
            "amount": {"type": "number"},
            "paid_amount": {"type": "number"},
            "status": {"type": "string"},
            "currency": {"type": "string"},
            "payment_method": {"type": "string"},
            "customer": CustomerSchema.validate_get(),
            "last_transaction": TransactionSchema.validate_get(),
        },
        "required": ["customer", "last_transaction"],
    }

    @classmethod
    def validate_get(cls):
        return cls.__get
