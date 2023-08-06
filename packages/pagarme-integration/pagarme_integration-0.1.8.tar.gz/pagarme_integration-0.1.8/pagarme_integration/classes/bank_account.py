from pagarme_integration.schemas.default_bank_account import DefauktBankAccountSchema
from pagarme_integration.utils.handle_errors import handle_error_pagarme
from pagarme_integration.classes.config import Config

from jsonschema import validate

from abc import abstractmethod

import requests
import json


class BankAccount(DefauktBankAccountSchema):
    __url_additional = "/recipients/ /default-bank-account"

    def __init__(
        self,
        bank_account,
        id,
        name,
        email,
        description,
        document,
        type,
        payment_mode,
        status,
        default_bank_account,
    ) -> None:
        if bank_account:
            self.bank_account = bank_account
        else:
            self.id = id
            self.name = name
            if email:
                self.email = email
            if description:
                self.description = description
            self.document = document
            self.type = type
            if payment_mode:
                self.payment_mode = payment_mode
            self.status = status
            self.default_bank_account = default_bank_account

    @abstractmethod
    def mount_obj(content: dict):
        return BankAccount(
            bank_account=content.get("bank_account"),
            id=content.get("id"),
            name=content.get("name"),
            email=content.get("email"),
            description=content.get("description"),
            document=content.get("document"),
            type=content.get("type"),
            payment_mode=content.get("payment_mode"),
            status=content.get("status"),
            default_bank_account=content.get("default_bank_account"),
        ).__dict__

    @classmethod
    def url_with_pk(cls, recipient_id) -> None:
        return cls.__url_additional.replace(" ", recipient_id)

    @classmethod
    def update(cls, recipient_id, payload):
        url = Config.get_url() + cls.url_with_pk(recipient_id=recipient_id)
        header = Config.get_header()
        header["Content-Type"] = "application/json"
        content = json.loads(
            requests.patch(
                url,
                auth=Config.get_auth(),
                headers=header,
                json=payload,
            ).text
        )
        content_validated = handle_error_pagarme(content)
        validate(instance=content_validated, schema=cls.validate_api_response())
        return cls.mount_obj(content_validated)
