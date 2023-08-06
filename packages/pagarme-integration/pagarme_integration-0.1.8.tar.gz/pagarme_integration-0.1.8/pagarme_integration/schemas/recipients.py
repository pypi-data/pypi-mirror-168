from pagarme_integration.schemas.automatic_anticipation_settings import (
    AutomaticAnticipationSettingsSchema,
)
from pagarme_integration.schemas.default_bank_account import DefauktBankAccountSchema
from pagarme_integration.schemas.transfer_settings import TransferSettingsSchema


class RecipientSchema:
    __insert = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "email": {"type": "string"},
            "description": {"type": "string"},
            "document": {"type": "string"},
            "type": {"type": "string"},
            "default_bank_account": DefauktBankAccountSchema.validate_insert(),
            "transfer_settings": TransferSettingsSchema.validate_get(),
            "automatic_anticipation_settings": AutomaticAnticipationSettingsSchema.validate_get(),
        },
        "required": ["name", "email", "document", "type", "default_bank_account"],
    }

    __update = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "email": {"type": "string"},
            "description": {"type": "string"},
            "type": {"type": "string"},
        },
        "required": ["name", "type"],
    }

    __get_only = {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "name": {"type": "string"},
            "email": {"type": "string"},
            "description": {"type": "string"},
            "type": {"type": "string"},
            "payment_mode": {"type": "string"},
            "status": {"type": "string"},
        },
        "required": ["id", "name", "type", "status"],
    }

    __get = {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "name": {"type": "string"},
            "email": {"type": "string"},
            "document": {"type": "string"},
            "type": {"type": "string"},
            "payment_mode": {"type": "string"},
            "status": {"type": "string"},
            "transfer_settings": TransferSettingsSchema.validate_get(),
            "default_bank_account": DefauktBankAccountSchema.validate_get(),
            "automatic_anticipation_settings": AutomaticAnticipationSettingsSchema.validate_get(),
        },
        "required": [
            "id",
            "name",
            "document",
            "type",
            "payment_mode",
            "status",
            "transfer_settings",
            "default_bank_account",
        ],
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

    @classmethod
    def validate_update(cls):
        return cls.__update

    @classmethod
    def validate_get_only(cls):
        return cls.__get_only
