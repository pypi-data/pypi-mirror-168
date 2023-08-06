import re
import jtd
import random
import string
import requests

from requests.adapters import HTTPAdapter, Retry

from .payload import normalize_checkout_session_payload as from_loose_checkout_session_payload
from .schemas.simple_checkout_session_payload import simple_checkout_session_payload_schema

public_key_pattern = re.compile("^pk_(test|live)_[0-9a-zA-Z]+$")
secret_key_pattern = re.compile("^sk_(test|live)_[0-9a-zA-Z]+$")
checkout_id_pattern = re.compile("^checkout_(test|live)_[0-9a-zA-Z]+$")
order_id_pattern = re.compile("^order_(test|live)_[0-9a-zA-Z]+$")
payment_id_pattern = re.compile("^payment_(test|live)_[0-9a-zA-Z]+$")
refund_id_pattern = re.compile("^refund_(test|live)_[0-9a-zA-Z]+$")
webhook_endpoint_id_pattern = re.compile(
    "^webhookendpoint_(test|live)_[0-9a-zA-Z]+$")
coupon_id_pattern = re.compile(
    "^coupon_(test|live)_[0-9a-zA-Z]+$")
promotion_code_id_pattern = re.compile(
    "^promotioncode_(test|live)_[0-9a-zA-Z]+$")


def valid_public_api_key(input):
    return bool(public_key_pattern.match(input))


def valid_secret_api_key(input):
    return bool(secret_key_pattern.match(input))


def valid_checkout_id(input):
    return bool(checkout_id_pattern.match(input))


def valid_order_id(input):
    return bool(order_id_pattern.match(input))


def valid_payment_id(input):
    return bool(payment_id_pattern.match(input))


def valid_refund_id(input):
    return bool(refund_id_pattern.match(input))


def valid_webhook_endpoint_id(input):
    return bool(webhook_endpoint_id_pattern.match(input))


def valid_coupon_id(input):
    return bool(coupon_id_pattern.match(input))


def valid_promotion_code_id(input):
    return bool(promotion_code_id_pattern.match(input))


def validate_checkout_session_payload(payload):
    errors = jtd.validate(
        schema=simple_checkout_session_payload_schema, instance=remove_none(payload))

    if len(payload['items']) == 0:
        errors.append('payload.items is required.')

    return errors


def get_currency(payload):
    currency = payload.get('currency', None)

    if not currency:
        items = payload.get('items', [])

        if len(items) > 0:
            currency = items[0].get('currency', None)

    return currency


def normalize_checkout_session_payload(input):
    payload = from_loose_checkout_session_payload(dict(input))
    shipping_info = payload.get('shippingInfo', {})
    currency = get_currency(payload)

    if not currency:
        raise Exception('Currency is not available.')

    if not payload.get('currency', None):
        payload['currency'] = currency

    if not shipping_info.get('feeCurrency'):
        shipping_info['feeCurrency'] = currency

    fee_currency = shipping_info.get('feeCurrency', None)
    fee_amount = shipping_info.get('feeAmount', None)
    shipping = fee_amount if fee_currency == currency and fee_amount else 0

    if not payload.get('amount', None):
        def get_price(item):
            item_currency = item.get('currency', None)

            if not item_currency:
                item['currency'] = currency
                item_currency = currency

            if item_currency != currency:
                raise Exception('Currency of all items should be the same.')

            sign = -1 if item.get('kind', 'product') == 'discount' else 1

            return item.get('amount', 0) * item.get('quantity', 1) * sign

        payload['amount'] = sum(
            list(map(get_price, payload.get('items', [])))) + shipping

    return payload


def jtd_error_to_deta(errors=[], prefix=''):
    def transator(error):
        instancePath = error.get('instancePath', None)
        schemaPath = error.get('schemaPath', None)

        if instancePath and schemaPath:
            return '%s.%s is invalid (%s)' % (prefix, '.'.join(instancePath), schemaPath)

        return error

    return map(transator, errors)


def remove_none(obj):
    if isinstance(obj, (list, tuple, set)):
        return type(obj)(remove_none(x) for x in obj if x is not None)
    elif isinstance(obj, dict):
        return type(obj)((remove_none(k), remove_none(v))
                         for k, v in obj.items() if k is not None and v is not None)
    else:
        return obj


def nonce():
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(15))


def retry_requests():
    retries = 1
    backoff_factor = 1,
    status_forcelist = [500, 501, 502, 503, 504],

    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    return session
