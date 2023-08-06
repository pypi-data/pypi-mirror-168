class DefauktBankAccountSchema:
    __insert = {
        "type": "object",
        "properties": {
            "holder_name": {"type": "string"},
            "bank": {"type": "string"},
            "branch_number": {"type": "string"},
            "branch_check_digit": {"type": "string"},
            "account_number": {"type": "string"},
            "account_check_digit": {"type": "string"},
            "holder_type": {"type": "string"},
            "holder_document": {"type": "string"},
            "type": {"type": "string"},
            "status": {"type": "string"},
        },
        "required": [
            "holder_name",
            "bank",
            "branch_number",
            "account_number",
            "account_check_digit",
            "holder_type",
            "holder_document",
            "type",
        ],
    }

    __bank_account = {
        "type": "object",
        "properties": {"bank_account": __insert},
        "required": ["bank_account"],
    }

    __get = {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "holder_name": {"type": "string"},
            "bank": {"type": "string"},
            "branch_number": {"type": "string"},
            "account_number": {"type": "string"},
            "account_check_digit": {"type": "string"},
            "holder_type": {"type": "string"},
            "holder_document": {"type": "string"},
            "type": {"type": "string"},
            "status": {"type": "string"},
        },
        "required": [
            "holder_name",
            "bank",
            "branch_number",
            "account_number",
            "account_check_digit",
            "holder_type",
            "holder_document",
            "type",
            "status",
        ],
    }

    __get_with_recipient = {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "holder_name": {"type": "string"},
            "bank": {"type": "string"},
            "branch_number": {"type": "string"},
            "account_number": {"type": "string"},
            "account_check_digit": {"type": "string"},
            "holder_type": {"type": "string"},
            "holder_document": {"type": "string"},
            "type": {"type": "string"},
            "status": {"type": "string"},
        },
        "required": [
            "holder_name",
            "bank",
            "branch_number",
            "account_number",
            "account_check_digit",
            "holder_type",
            "holder_document",
            "type",
            "status",
        ],
    }

    __api_response = {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "name": {"type": "string"},
            "email": {"type": "string"},
            "description": {"type": "string"},
            "document": {"type": "string"},
            "type": {"type": "string"},
            "payment_mode": {"type": "string"},
            "status": {"type": "string"},
            "default_bank_account": __get,
        },
        "required": [
            "id",
            "name",
            "email",
            "document",
            "type",
            "status",
            "default_bank_account",
        ],
    }

    @classmethod
    def validate_get(cls):
        return cls.__get

    @classmethod
    def validate_insert(cls):
        return cls.__insert

    @classmethod
    def validate_update(cls):
        return cls.__bank_account

    @classmethod
    def validate_api_response(cls):
        return cls.__api_response

    @classmethod
    def validate_get_with_recipient(cls):
        return cls.__get_with_recipient
