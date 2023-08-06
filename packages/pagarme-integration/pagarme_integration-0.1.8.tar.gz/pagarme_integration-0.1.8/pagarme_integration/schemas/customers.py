from pagarme_integration.schemas.phone import PhoneSchema


class CustomerSchema:
    __insert = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "email": {"type": "string"},
            "document": {"type": "string"},
            "document_type": {"type": "string"},
            "type": {"type": "string"},
            "phones": PhoneSchema.validate_insert(),
        },
        "required": ["name", "email", "document", "type", "phones"],
    }

    __get = {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "name": {"type": "string"},
            "email": {"type": "string"},
            "document": {"type": "string"},
            "document_type": {"type": "string"},
            "type": {"type": "string"},
        },
        "required": ["id", "name"],
    }

    __list = {"type": "array", "items": __get}

    @classmethod
    def validate_insert(cls):
        return cls.__insert

    @classmethod
    def validate_get(cls):
        return cls.__get

    @classmethod
    def validate_list(cls):
        return cls.__list
