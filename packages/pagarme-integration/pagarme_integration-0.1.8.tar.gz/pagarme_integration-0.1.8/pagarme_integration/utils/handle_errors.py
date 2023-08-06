from jsonschema.exceptions import ValidationError


def handle_error_pagarme(content: dict) -> dict:
    if content.get("errors"):
        raise ValidationError(message=sum(content.get("errors").values(), [])[0])
    elif content.get("message"):
        raise ValidationError(message=content.get("message"))
    return content


def handle_error_insert_orders(content: dict) -> None:
    if content.get("errors"):
        raise ValidationError(message=content.get("errors")[0].get("message"))


def handle_error_serializer(errors: dict) -> dict:
    return {
        "detail": [
            f"{keys}:{str(v)}" for keys, values in errors.items() for v in values
        ]
    }
