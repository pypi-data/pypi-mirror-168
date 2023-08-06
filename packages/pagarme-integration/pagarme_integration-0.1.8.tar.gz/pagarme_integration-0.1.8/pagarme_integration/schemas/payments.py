from pagarme_integration.schemas.cards import CardSchema
from pagarme_integration.schemas.pix import PixSchema


class PaymentSchema:
    __options = {
        "type": "object",
        "properties": {
            "charge_processing_fee": {"type": "boolean"},
            "charge_remainder_fee": {"type": "boolean"},
            "liable": {"type": "boolean"},
        },
        "required": ["charge_processing_fee", "charge_remainder_fee", "liable"],
    }
    __split = {
        "type": "object",
        "properties": {
            "options": __options,
            "type": {"type": "string"},
            "amount": {"type": "string"},
            "recipient_id": {"type": "string"},
        },
        "required": ["options", "type", "amount", "recipient_id"],
    }

    __get = {
        "type": "object",
        "properties": {
            "payment_method": {"type": "string"},
            "credit_card": CardSchema.validate_credit_card(),
            "pix": PixSchema.validate_get(),
            "split": {"type": "array", "items": __split},
        },
        "required": ["payment_method"],
    }

    @classmethod
    def validate_get(cls):
        return cls.__get
