from pagarme_integration.schemas.errors import ErrorSchema


class GatewayResponseSchema:
    __get = {
        "type": "object",
        "properties": {
            "code": {"type": "string"},
            "errors": {"type": "array", "items": ErrorSchema.validate_get()},
        },
        "required": ["code", "errors"],
    }

    @classmethod
    def validate_get(cls):
        return cls.__get
