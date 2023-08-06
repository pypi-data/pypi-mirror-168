def omit(obj, omitKeys):
    rest = obj.copy()

    for key in omitKeys:
        try:
            del rest[key]
        except:
            pass

    return rest


def normalize_customer_info(customer=None):
    if customer is None:
        customer = {}

    normalized_customer = {
        'accountAge': customer.get('accountAge', None),
        'emailAddress': customer.get('emailAddress', None),
        'firstName': customer.get('firstName', None),
        'lastName': customer.get('lastName', None),
        'firstNameKana': customer.get('firstNameKana', None),
        'lastNameKana': customer.get('lastNameKana', None),
        'address': customer.get('address', None),
        'phoneNumber': customer.get('phoneNumber'),
        'dateOfBirth': customer.get('dateOfBirth', None),
        'legalGender': customer.get('legalGender'),
        'reference': customer.get('reference', None),
    }

    rest = omit(customer, [
        'accountAge',
        'emailAddress',
        'firstName',
        'lastName',
        'firstNameKana',
        'lastNameKana',
        'address',
        'phoneNumber',
        'dateOfBirth',
        'legalGender',
        'reference',
    ])

    return {**rest, **normalized_customer}


def normalize_discount_item(item=None):
    if item is None:
        item = {}

    normalized_item = {
        'name': item.get('name', None),
        'description': item.get('description', None),
        'amount': item.get('amount', None),
        'currency': item.get('currency', None),
    }

    rest = omit(item, [
        'name',
        'description',
        'amount',
        'currency',
    ])

    return {**rest, **normalized_item}


def normalize_tax_item(item=None):
    if item is None:
        item = {}

    normalized_item = {
        'name': item.get('name', None),
        'description': item.get('description', None),
        'amount': item.get('amount', None),
        'currency': item.get('currency', None),
    }

    rest = omit(item, [
        'name',
        'description',
        'amount',
        'currency',
    ])

    return {**rest, **normalized_item}


def normalize_product_item(item=None):
    if item is None:
        item = {}

    normalized_item = {
        'quantity': item.get('quantity', None),
        'name': item.get('name', None),
        'brand': item.get('brand', None),
        'categories': item.get('categories', None),
        'gtin': item.get('gtin', None),
        'images': item.get('images', None),
        'reference': item.get('reference', None),
        'url': item.get('url', None),
        'amount': item.get('amount', None),
        'currency': item.get('currency', None),
        'label': item.get('label', None),
        'description': item.get('description', None),
        'metadata': item.get('metadata', None),
        'productDescription': item.get('productDescription', None),
        'productMetadata': item.get('productMetadata', None),
        'priceDescription': item.get('priceDescription', None),
        'priceMetadata': item.get('priceMetadata', None),
    }

    rest = omit(item, [
        'quantity',
        'name',
        'brand',
        'categories',
        'gtin',
        'images',
        'reference',
        'url',
        'amount',
        'currency',
        'label',
        'description',
        'metadata',
        'productDescription',
        'productMetadata',
        'priceDescription',
        'priceMetadata',
    ])

    return {**rest, **normalized_item}


def normalize_item(item=None):
    if item is None:
        item = {}

    kind = item.get('kind', 'product')

    if kind == 'discount':
        return normalize_discount_item(item)
    elif kind == 'tax':
        return normalize_tax_item(item)
    else:
        return normalize_product_item(item)


def normalize_items(items=None):
    if items is None:
        items = []

    return list(map(normalize_item, items)) if type(items) is list else []


def normalize_address(address):
    if address is None:
        address = {}

    normalized_address = {
        'line1': address.get('line1', None),
        'line2': address.get('line2', None),
        'line3': address.get('line3', None),
        'line4': address.get('line4', None),
        'line5': address.get('line5', None),
        'subLocality': address.get('subLocality', None),
        'locality': address.get('locality', None),
        'administrativeArea': address.get('administrativeArea', None),
        'postalCode': address.get('postalCode', None),
        'country': address.get('country', None),
    }

    rest = omit(address, [
        'line1',
        'line2',
        'line3',
        'line4',
        'line5',
        'subLocality',
        'locality',
        'administrativeArea',
        'postalCode',
        'country',
    ])

    return {**rest, **normalized_address}


def normalize_shipping_info(shipping):
    if shipping is None:
        shipping = {}

    normalized_shipping = {
        'address': normalize_address(shipping.get('address', None)),
        'addressType': shipping.get('addressType', None),
        'feeAmount': shipping.get('feeAmount', None),
        'feeCurrency': shipping.get('feeCurrency', None),
    }

    rest = omit(shipping, [
        'address',
        'addressType',
        'feeAmount',
        'feeCurrency',
    ])

    return {**rest, **normalized_shipping}


def normalize_checkout_session_payload(payload):
    if payload is None:
        payload = {}

    normalized_payload = {
        'amount': payload.get('amount', None),
        'currency': payload.get('currency', None),
        'captureMethod': payload.get('captureMethod', None),
        'items': normalize_items(payload.get('items', None)),
        'customerInfo': normalize_customer_info(payload.get('customerInfo', None)),
        'shippingInfo': normalize_shipping_info(payload.get('shippingInfo', None)),
        'reference': payload.get('reference', None),
        'description': payload.get('description', None),
        'metadata': payload.get('metadata', None),
        'successUrl': payload.get('successUrl', None),
        'cancelUrl': payload.get('cancelUrl', None),
    }

    rest = omit(payload, [
        'amount',
        'currency',
        'captureMethod',
        'items',
        'customerInfo',
        'shippingInfo',
        'reference',
        'description',
        'metadata',
        'successUrl',
        'cancelUrl',
    ])

    return {**rest, **normalized_payload}
