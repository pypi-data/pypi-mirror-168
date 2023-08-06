import json
from abc import abstractmethod

import requests
from jsonschema import validate
from pagarme_integration.classes.config import Config
from pagarme_integration.schemas.withdraw import WithdrawSchema
from pagarme_integration.utils.handle_errors import handle_error_pagarme


class Withdraw(WithdrawSchema):
    __url_additional = "/recipients/ /withdrawals"

    def __init__(self, id, amount, status, bank_account) -> None:
        if id:
            self.id = id
        self.amount = amount
        if status:
            self.status = status
        if bank_account:
            self.bank_account = bank_account

    @abstractmethod
    def mount_obj(content: dict):
        return Withdraw(
            id=content.get("id"),
            amount=content.get("amount"),
            status=content.get("status"),
            bank_account=content.get("bank_account"),
        ).__dict__

    @classmethod
    def url_with_pk(cls, recipient_id) -> None:
        return cls.__url_additional.replace(" ", recipient_id)

    @classmethod
    def insert_withdraw(cls, recipient_id, payload):
        url = Config.get_url() + cls.url_with_pk(recipient_id=recipient_id)
        header = Config.get_header()
        header["Content-Type"] = "application/json"
        content = json.loads(
            requests.post(
                url,
                auth=Config.get_auth(),
                headers=header,
                json=payload,
            ).text
        )
        content_validated = handle_error_pagarme(content)
        validate(instance=content_validated, schema=cls.validate_get())
        return cls.mount_obj(content_validated)

    @classmethod
    def get_withdrawal(cls, recipient_id, withdraw_id):
        url = (
            Config.get_url()
            + cls.url_with_pk(recipient_id=recipient_id)
            + f"/{withdraw_id}"
        )
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

    @classmethod
    def get_withdrawals(cls, recipient_id, status):
        response = []
        if status:
            url = (
                Config.get_url()
                + cls.url_with_pk(recipient_id=recipient_id)
                + f"?{status}"
            )
        else:
            url = Config.get_url() + cls.url_with_pk(recipient_id=recipient_id)
        content = json.loads(
            requests.get(
                url,
                auth=Config.get_auth(),
                headers=Config.get_header(),
            ).text
        )
        content_validated = handle_error_pagarme(content)
        contents = content_validated.get("data")
        validate(instance=contents, schema=cls.validate_list())
        [response.append(Withdraw.mount_obj(content)) for content in contents]
        return response
