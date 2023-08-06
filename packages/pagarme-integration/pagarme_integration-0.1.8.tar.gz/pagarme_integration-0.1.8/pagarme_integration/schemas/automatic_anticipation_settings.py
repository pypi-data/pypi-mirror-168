class AutomaticAnticipationSettingsSchema:
    __get = {
        "type": "object",
        "properties": {
            "enabled": {"type": "boolean"},
            "type": {"type": "string"},
            "volume_percentage": {"type": "number"},
            "delay": {"type": "number"},
        },
        "required": [
            "enabled",
            "type",
            "volume_percentage",
            "delay",
        ],
    }

    @classmethod
    def validate_get(cls):
        return cls.__get
