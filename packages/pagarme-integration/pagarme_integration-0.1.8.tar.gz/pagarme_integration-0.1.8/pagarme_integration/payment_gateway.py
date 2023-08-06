from jsonschema import validate
from jsonschema.exceptions import SchemaError, ValidationError

from pagarme_integration.classes.balance import Balance
from pagarme_integration.classes.bank_account import BankAccount
from pagarme_integration.classes.cards import Card
from pagarme_integration.classes.config import Config
from pagarme_integration.classes.customers import Customer
from pagarme_integration.classes.orders import Order
from pagarme_integration.classes.recipients import Recipient
from pagarme_integration.classes.withdraw import Withdraw


class PaymentGatewayClass:
    def __init__(self, key) -> None:
        Config.set_auth(key=key)

    def get_withdrawal(self, recipient_id, withdraw_id):
        return Withdraw.get_withdrawal(
            recipient_id=recipient_id, withdraw_id=withdraw_id
        )

    def get_withdrawals(self, recipient_id, status=None):
        return Withdraw.get_withdrawals(recipient_id=recipient_id, status=status)

    def insert_withdraw(self, recipient_id, payload):
        try:
            validate(instance=payload, schema=Withdraw.validate_insert())
            return Withdraw.insert_withdraw(
                recipient_id=recipient_id, payload=Withdraw.mount_obj(content=payload)
            )
        except ValidationError as ve:
            raise ve
        except SchemaError as se:
            raise se

    def get_recipient(self, recipient_id):
        return Recipient.get_recipient(pk=recipient_id)

    def insert_recipient(self, payload):
        try:
            validate(instance=payload, schema=Recipient.validate_insert())
            return Recipient.insert_recipient(
                payload=Recipient.mount_obj(content=payload)
            )
        except ValidationError as ve:
            raise ve
        except SchemaError as se:
            raise se

    def update_recipient(self, recipient_id, payload):
        try:
            validate(instance=payload, schema=Recipient.validate_update())
            return Recipient.update_recipient(
                pk=recipient_id, payload=Recipient.mount_obj(content=payload)
            )
        except ValidationError as ve:
            raise ve
        except SchemaError as se:
            raise se

    def update_bank_account(self, recipient_id, payload):
        try:
            validate(instance=payload, schema=BankAccount.validate_update())
            return BankAccount.update(
                recipient_id=recipient_id,
                payload=BankAccount.mount_obj(content=payload),
            )
        except ValidationError as ve:
            raise ve
        except SchemaError as se:
            raise se

    def get_balance(self, recipient_id):
        return Balance.get_balance(recipient_id=recipient_id)

    # def get_customers(self):
    #    return Customer.get_customers()

    def get_customer(self, customer_id):
        return Customer.get_customer(pk=customer_id)

    def insert_customer(self, payload):
        try:
            validate(instance=payload, schema=Customer.validate_insert())
            return Customer.insert_customer(payload=Customer.mount_obj(content=payload))
        except ValidationError as ve:
            raise ve
        except SchemaError as se:
            raise se

    def get_cards(self, customer_id):
        return Card.get_cards(customer_id=customer_id)

    def get_card(self, customer_id, card_id):
        return Card.get_card(customer_id=customer_id, pk=card_id)

    def insert_card(self, customer_id, payload):
        try:
            validate(instance=payload, schema=Card.validate_insert())
            return Card.insert_card(
                customer_id=customer_id, payload=Card.mount_obj(content=payload)
            )
        except ValidationError as ve:
            raise ve

    def get_orders(self, customer_id):
        return Order.get_orders(customer_id=customer_id)

    def get_order(self, order_id):
        return Order.get_order(pk=order_id)

    def insert_order(self, payload):
        try:
            validate(instance=payload, schema=Order.validate_insert())
            return Order.insert_order(payload=Order.mount_obj(content=payload))
        except ValidationError as ve:
            raise ve
