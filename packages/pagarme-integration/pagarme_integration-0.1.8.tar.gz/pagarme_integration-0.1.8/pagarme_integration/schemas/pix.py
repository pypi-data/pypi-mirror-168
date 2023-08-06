class PixSchema:
    __additional_information = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "value": {"type": "string"},
        },
        "required": ["name", "value"],
    }

    __get = {
        "type": "object",
        "properties": {
            "expires_in": {"type": "string"},
            "expires_at": {"type": "string"},
            "additional_information": __additional_information,
        },
        "required": ["expires_in"],
    }

    @classmethod
    def validate_get(cls):
        return cls.__get
