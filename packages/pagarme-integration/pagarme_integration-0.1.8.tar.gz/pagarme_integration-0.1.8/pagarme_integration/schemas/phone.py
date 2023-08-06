class PhoneSchema:
    __get = {
        "type": "object",
        "properties": {
            "country_code": {"type": "string"},
            "area_code": {"type": "string"},
            "number": {"type": "string"},
        },
        "required": ["country_code", "area_code", "number"],
    }
    __insert = {
        "type": "object",
        "properties": {
            "home_phone": __get,
            "mobile_phone": __get,
        },
        "required": ["mobile_phone"],
    }

    @classmethod
    def validate_insert(cls):
        return cls.__insert

    @classmethod
    def validate_get(cls):
        return cls.__get
