from pagarme_integration.schemas.address import BillingAddressSchema


class CardSchema:
    __insert = {
        "type": "object",
        "properties": {
            "number": {"type": "string"},
            "holder_name": {"type": "string"},
            "exp_month": {"type": "number"},
            "exp_year": {"type": "number"},
            "cvv": {"type": "string"},
            "billing_address": BillingAddressSchema.validate_insert(),
        },
        "required": [
            "number",
            "holder_name",
            "exp_month",
            "exp_year",
            "cvv",
            "billing_address",
        ],
    }

    __get = {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "holder_name": {"type": "string"},
            "exp_month": {"type": "number"},
            "exp_year": {"type": "number"},
            "last_four_digits": {"type": "string"},
        },
        "required": ["id", "holder_name", "exp_month", "exp_year", "last_four_digits"],
    }

    __list = {"type": "array", "items": __get}

    __cvv = {
        "type": "object",
        "properties": {
            "cvv": {"type": "string"},
        },
        "required": ["cvv"],
    }
    __credit_card = {
        "type": "object",
        "properties": {
            "capture": {"type": "boolean"},
            "statement_descriptor": {"type": "string"},
            "card_id": {"type": "string"},
            "card": __cvv,
        },
        "required": ["capture", "statement_descriptor", "card_id", "card"],
    }

    @classmethod
    def validate_insert(cls):
        return cls.__insert

    @classmethod
    def validate_get(cls):
        return cls.__get

    @classmethod
    def validate_list(cls):
        return cls.__list

    @classmethod
    def validate_cvv(cls):
        return cls.__cvv

    @classmethod
    def validate_credit_card(cls):
        return cls.__credit_card
