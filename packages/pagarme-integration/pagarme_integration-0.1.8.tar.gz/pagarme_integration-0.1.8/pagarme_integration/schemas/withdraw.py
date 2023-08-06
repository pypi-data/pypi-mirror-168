from pagarme_integration.schemas.default_bank_account import DefauktBankAccountSchema


class WithdrawSchema:
    __insert = {
        "type": "object",
        "properties": {
            "amount": {"type": "number"},
        },
        "required": [
            "amount",
        ],
    }

    __get = {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "amount": {"type": "number"},
            "status": {"type": "string"},
            "bank_account": DefauktBankAccountSchema.validate_get_with_recipient(),
        },
        "required": [
            "id",
            "amount",
            "status",
            "bank_account",
        ],
    }

    __list = {"type": "array", "items": __get}

    @classmethod
    def validate_get(cls):
        return cls.__get

    @classmethod
    def validate_insert(cls):
        return cls.__insert

    @classmethod
    def validate_list(cls):
        return cls.__list
