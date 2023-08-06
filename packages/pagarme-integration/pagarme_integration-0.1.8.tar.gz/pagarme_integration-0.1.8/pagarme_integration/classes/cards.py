from pagarme_integration.utils.handle_errors import handle_error_pagarme
from pagarme_integration.schemas.cards import CardSchema
from pagarme_integration.classes.config import Config

from jsonschema import validate

from abc import abstractmethod

import requests
import json


class Card(CardSchema):
    def __init__(
        self,
        id,
        number,
        holder_name,
        exp_month,
        exp_year,
        last_four_digits,
        cvv,
        billing_address,
    ) -> None:
        if id:
            self.id = id
        if number:
            self.number = number
        self.holder_name = holder_name
        self.exp_month = exp_month
        self.exp_year = exp_year
        if last_four_digits:
            self.last_four_digits = last_four_digits
        if cvv:
            self.cvv = cvv
        if billing_address:
            self.billing_address = billing_address

    @abstractmethod
    def mount_obj(content: dict):
        return Card(
            id=content.get("id"),
            number=content.get("number"),
            holder_name=content.get("holder_name"),
            exp_month=content.get("exp_month"),
            exp_year=content.get("exp_year"),
            last_four_digits=content.get("last_four_digits"),
            cvv=content.get("cvv"),
            billing_address=content.get("billing_address"),
        ).__dict__

    @classmethod
    def get_cards(cls, customer_id):
        response = []
        url = Config.get_url() + f"/customers/{customer_id}/cards"
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
        [response.append(Card.mount_obj(content)) for content in contents]
        return response

    @classmethod
    def get_card(cls, customer_id, pk):
        url = Config.get_url() + f"/customers/{customer_id}/cards/{pk}"
        content = json.loads(
            requests.get(
                url,
                auth=Config.get_auth(),
                headers=Config.get_header(),
            ).text
        )
        content_validated = handle_error_pagarme(content)
        validate(instance=content_validated, schema=cls.validate_get())
        return Card.mount_obj(content_validated)

    @classmethod
    def insert_card(cls, customer_id, payload):
        url = Config.get_url() + f"/customers/{customer_id}/cards"
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
        return Card.mount_obj(content_validated)
