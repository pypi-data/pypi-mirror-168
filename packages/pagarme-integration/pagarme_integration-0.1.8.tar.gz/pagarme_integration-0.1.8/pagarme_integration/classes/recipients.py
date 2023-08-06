from pagarme_integration.utils.handle_errors import handle_error_pagarme
from pagarme_integration.schemas.recipients import RecipientSchema
from pagarme_integration.classes.config import Config

from jsonschema import validate

from abc import abstractmethod

import requests
import json


class Recipient(RecipientSchema):
    __url_additional = "/recipients"

    def __init__(
        self,
        id,
        name,
        email,
        description,
        document,
        type,
        payment_mode,
        status,
        transfer_settings,
        default_bank_account,
        automatic_anticipation_settings,
    ) -> None:
        if id:
            self.id = id
        if name:
            self.name = name
        if email:
            self.email = email
        if description:
            self.description = description
        if document:
            self.document = document
        if type:
            self.type = type
        if payment_mode:
            self.payment_mode = payment_mode
        if status:
            self.status = status
        if transfer_settings:
            self.transfer_settings = transfer_settings
        if default_bank_account:
            self.default_bank_account = default_bank_account
        if automatic_anticipation_settings:
            self.automatic_anticipation_settings = automatic_anticipation_settings

    @abstractmethod
    def mount_obj(content: dict):
        return Recipient(
            id=content.get("id"),
            name=content.get("name"),
            email=content.get("email"),
            description=content.get("description"),
            document=content.get("document"),
            type=content.get("type"),
            transfer_settings=content.get("transfer_settings"),
            payment_mode=content.get("payment_mode"),
            status=content.get("status"),
            default_bank_account=content.get("default_bank_account"),
            automatic_anticipation_settings=content.get(
                "automatic_anticipation_settings"
            ),
        ).__dict__

    @classmethod
    def url_with_pk(cls, pk) -> None:
        return f"{cls.__url_additional}/{pk}"

    @classmethod
    def get_recipient(cls, pk):
        url = Config.get_url() + cls.url_with_pk(pk=pk)
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
    def insert_recipient(cls, payload):
        url = Config.get_url() + "/recipients"
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
    def update_recipient(cls, pk, payload):
        url = Config.get_url() + cls.url_with_pk(pk=pk)
        header = Config.get_header()
        header["Content-Type"] = "application/json"
        content = json.loads(
            requests.put(
                url,
                auth=Config.get_auth(),
                headers=header,
                json=payload,
            ).text
        )
        content_validated = handle_error_pagarme(content)
        validate(instance=content_validated, schema=cls.validate_get())
        return cls.mount_obj(content_validated)
