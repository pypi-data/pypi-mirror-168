from pagarme_integration.schemas.recipients import RecipientSchema


class BalanceSchema:
    __get = {
        "type": "object",
        "properties": {
            "currency": {"type": "string"},
            "available_amount": {"type": "number"},
            "waiting_funds_amount": {"type": "number"},
            "transferred_amount": {"type": "number"},
            "recipient": RecipientSchema.validate_get_only(),
        },
        "required": [
            "currency",
            "available_amount",
            "waiting_funds_amount",
            "transferred_amount",
            "recipient",
        ],
    }

    @classmethod
    def validate_get(cls):
        return cls.__get
