import jtd

simple_checkout_session_payload_schema = jtd.Schema.from_dict({
    "definitions": {
        "address": {
            "properties": {
                "line1": {"type": "string"},
                "locality": {"type": "string"},
                "country": {"type": "string"},
                "postalCode": {"type": "string"}
            },
            "optionalProperties": {
                "line2": {"type": "string"},
                "line3": {"type": "string"},
                "line4": {"type": "string"},
                "line5": {"type": "string"},
                "administrativeArea": {"type": "string"},
                "subLocality": {"type": "string"},
                "addressType": {"type": "string"}
            },
            "additionalProperties": True
        },
        "customer": {
            "optionalProperties": {
                "accountAge": {"type": "uint32"},
                "emailAddress": {"type": "string"},
                "firstName": {"type": "string"},
                "lastName": {"type": "string"},
                "phoneNumber": {"type": "string"},
                "firstNameKana": {"type": "string"},
                "lastNameKana": {"type": "string"},
                "address": {"ref": "address"},
                "dateOfBirth": {"type": "string"},
                "legalGender": {"type": "string"},
                "reference": {"type": "string"}
            },
            "additionalProperties": True
        },
        "lineItem": {
            "optionalProperties": {
                "kind": {"type": "string"},

                "name": {"type": "string"},
                "quantity": {"type": "uint16"},
                "amount": {"type": "uint32"},
                "currency": {"type": "string"},

                "description": {"type": "string"},
                "priceDescription": {"type": "string"},
                "productDescription": {"type": "string"},
                "label": {"type": "string"},

                "brand": {"type": "string"},
                "categories": {"elements": {"type": "string"}},
                "gtin": {"type": "string"},
                "images": {"elements": {"type": "string"}},
                "reference": {"type": "string"},
                "url": {"type": "string"}
            },
            "additionalProperties": True
        }
    },

    "properties": {
        "amount": {"type": "uint32"},
        "currency": {"type": "string"},

        "items": {"elements": {"ref": "lineItem"}},
        "customerInfo": {"ref": "customer"},
        "shippingInfo": {
            "properties": {
                "address": {"ref": "address"}
            },
            "optionalProperties": {
                "addressType": {"type": "string"},
                "feeAmount": {"type": "uint32"},
                "feeCurrency": {"type": "string"}
            },
            "additionalProperties": True
        }
    },
    "optionalProperties": {
        "captureMethod": {"type": "string"},
        "description": {"type": "string"},
        "reference": {"type": "string"},

        "successUrl": {"type": "string"},
        "cancelUrl": {"type": "string"}
    },
    "additionalProperties": True
}
)
