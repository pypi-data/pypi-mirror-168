class BillingAddressSchema:
    __insert = {
        "type": "object",
        "properties": {
            "country": {"type": "string"},
            "state": {"type": "string"},
            "city": {"type": "string"},
            "zip_code": {"type": "string"},
            "line_1": {"type": "string"},
            "line_2": {"type": "string"},
        },
        "required": ["country", "state", "city", "zip_code", "line_1"],
    }

    @classmethod
    def validate_insert(cls):
        return cls.__insert
