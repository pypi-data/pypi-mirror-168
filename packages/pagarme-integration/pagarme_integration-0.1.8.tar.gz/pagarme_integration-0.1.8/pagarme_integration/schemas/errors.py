class ErrorSchema:
    __get = {
        "type": "object",
        "properties": {
            "message": {"type": "string"},
        },
        "required": ["message"],
    }

    @classmethod
    def validate_get(cls):
        return cls.__get
