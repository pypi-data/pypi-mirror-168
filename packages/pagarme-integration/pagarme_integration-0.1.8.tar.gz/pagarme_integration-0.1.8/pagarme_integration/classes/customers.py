from pagarme_integration.utils.handle_errors import handle_error_pagarme
from pagarme_integration.schemas.customers import CustomerSchema
from pagarme_integration.classes.config import Config

from jsonschema import validate

from abc import abstractmethod

import requests
import json


class Customer(CustomerSchema):
    def __init__(self, id, name, email, document, document_type, type, phones) -> None:
        if id:
            self.id = id
        self.name = name
        if email:
            self.email = email
        if document:
            self.document = document
        if document_type:
            self.document_type = document_type
        if type:
            self.type = type
        if phones:
            self.phones = phones

    @abstractmethod
    def mount_obj(content: dict):
        return Customer(
            id=content.get("id"),
            name=content.get("name"),
            email=content.get("email"),
            document=content.get("document"),
            document_type=content.get("document_type"),
            type=content.get("type"),
            phones=content.get("phones"),
        ).__dict__

    @classmethod
    def get_customers(cls):
        response = []
        url = Config.get_url() + "/customers"
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
        [response.append(Customer.mount_obj(content)) for content in contents]
        return response

    @classmethod
    def get_customer(cls, pk):
        url = Config.get_url() + f"/customers/{pk}"
        content = json.loads(
            requests.get(
                url,
                auth=Config.get_auth(),
                headers=Config.get_header(),
            ).text
        )
        content_validated = handle_error_pagarme(content)
        validate(instance=content_validated, schema=cls.validate_get())
        return Customer.mount_obj(content_validated)

    @classmethod
    def insert_customer(cls, payload):
        url = Config.get_url() + "/customers"
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
        return Customer.mount_obj(content_validated)
