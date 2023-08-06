class ItemSchema:
    __get = {
        "type": "object",
        "properties": {
            "amount": {"type": "number"},
            "description": {"type": "string"},
            "quantity": {"type": "number"},
        },
        "required": ["amount", "description", "quantity"],
    }

    __insert = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "amount": {"type": "number"},
            "description": {"type": "string"},
            "quantity": {"type": "number"},
            "code": {"type": "string"},
        },
        "required": ["amount", "description", "quantity", "code"],
    }

    @classmethod
    def validate_get(cls):
        return cls.__get

    @classmethod
    def validate_insert(cls):
        return cls.__insert
