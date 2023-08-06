class TransferSettingsSchema:
    __get = {
        "type": "object",
        "properties": {
            "transfer_enabled": {"type": "boolean"},
            "transfer_interval": {"type": "string"},
            "transfer_day": {"type": "number"},
        },
        "required": [
            "transfer_enabled",
            "transfer_interval",
            "transfer_day",
        ],
    }

    @classmethod
    def validate_get(cls):
        return cls.__get
