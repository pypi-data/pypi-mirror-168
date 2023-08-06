import requests
from ping.helper.apiHelper import check_errors, json_deserialize


def create(headers, base_url, payment_link_id, obj):

    # Does a PUT request to /api/v1/payment_links/{payment_link_id}/invoice.

    # Creates an invoice for a payment link.
    # Args (provided by the tenant):
    #   payment_link_id (string, required): Id of a specific payment link.
    #   obj (json, required): json for creating a new payment link invoice.
    #   To obtain the necessary information, use the documentation.
    # Returns:
    #   Response: Empty response

    # Prepare and execute response
    _path = f'/api/v1/payment_links/{payment_link_id}/invoice'
    _url = base_url + _path
    response = requests.put(_url, headers=headers, json=obj)

    # deserialize and check errors
    decoded = json_deserialize(response.text)
    _result = check_errors(response, decoded)
    return _result


def get(headers, base_url, payment_link_id):
    # Does a GET request to /api/v1/payment_links/{payment_link_id}/invoice.

    # Retrieves a specific invoice.
    # Args (provided by the tenant):
    #   payment_link_id (String, required): Id of a specific payment link.
    # Returns:
    #   Response: A json object with a payment link as well as other
    #   useful information such as status codes, headers and a potential errors.

    # Prepare and execute response
    _path = f'/api/v1/payment_links/{payment_link_id}/invoice'
    _url = base_url + _path
    response = requests.get(_url, headers=headers)

    # deserialize and check errors
    decoded = json_deserialize(response.text)
    _result = check_errors(response, decoded)
    return _result
