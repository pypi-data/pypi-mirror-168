from pagarme_integration.schemas.balance import BalanceSchema
from pagarme_integration.utils.handle_errors import handle_error_pagarme
from pagarme_integration.classes.config import Config

from jsonschema import validate

from abc import abstractmethod

import requests
import json


class Balance(BalanceSchema):
    __url_additional = "/recipients/ /balance"

    def __init__(
        self,
        currency,
        available_amount,
        waiting_funds_amount,
        transferred_amount,
        recipient,
    ) -> None:
        self.currency = currency
        self.available_amount = available_amount
        self.waiting_funds_amount = waiting_funds_amount
        self.transferred_amount = transferred_amount
        self.recipient = recipient

    @abstractmethod
    def mount_obj(content: dict):
        return Balance(
            currency=content.get("currency"),
            available_amount=content.get("available_amount"),
            waiting_funds_amount=content.get("waiting_funds_amount"),
            transferred_amount=content.get("transferred_amount"),
            recipient=content.get("recipient"),
        ).__dict__

    @classmethod
    def url_with_pk(cls, recipient_id) -> None:
        return cls.__url_additional.replace(" ", recipient_id)

    @classmethod
    def get_balance(cls, recipient_id):
        url = Config.get_url() + cls.url_with_pk(recipient_id=recipient_id)
        content = json.loads(
            requests.get(
                url,
                auth=Config.get_auth(),
                headers=Config.get_header(),
            ).text
        )
        content_validated = handle_error_pagarme(content)
        validate(instance=content_validated, schema=cls.validate_get())
        return cls.mount_obj(content_validated)
