import requests
from ping.helper.apiHelper import json_deserialize, check_errors


def list(headers, base_url):
    # Does a GET request to /api/v1/payment_links.

    # Retrieves a list of payment Links.
    # Args (provided by the tenant):
    #   None arguments.
    # Returns:
    #   Response: A json object with the response value as well as other
    #   useful information such as status codes, headers and potential errors.

    # Prepare and execute response
    _path = '/api/v1/payment_links'
    _url = base_url + _path
    response = requests.get(_url, headers=headers)

    # deserialize and check errors
    decoded = json_deserialize(response.text)
    _result = check_errors(response, decoded)
    return _result


def create(headers, base_url, obj):
    # Does a POST request to /api/v1/payment_links.

    # Creates a new Payment Link.
    # Args (provided by the tenant):
    #    obj (json,required): A json object with with information that is required to create a
    #    Payment Link. To obtain the necessary information, use the documentation.
    # Returns:
    #    Response: A json object with the response value as well as other
    #    useful information such as status codes, headers and potential errors.

    # Prepare and execute response
    _path = '/api/v1/payment_links'
    _url = base_url + _path
    response = requests.post(_url, headers=headers, json=obj)

    # deserialize and check errors
    decoded = json_deserialize(response.text)
    _result = check_errors(response, decoded)
    return _result


def get(headers, base_url, payment_link_id):
    # Does a GET request to /api/v1/payment_links/{payment_link_id}.

    # Retrieves a specific Payment Link.
    # Args (provided by the tenant):
    #    payment_link_id (String, required): The ID of the of the Payment Link to retrieve.
    # Returns:
    #    Response: A json object with the response value as well as other
    #    useful information such as status codes, headers and a potential errors.

    # Prepare and execute response
    _path = f'/api/v1/payment_links/{payment_link_id}'
    _url = base_url + _path
    response = requests.get(_url, headers=headers)

    # deserialize and check errors
    decoded = json_deserialize(response.text)
    _result = check_errors(response, decoded)
    return _result


def cancel(headers, base_url, payment_link_id):
    # Does a PUT request to /api/v1/payment_links/{payment_link_id}/cancel.

    # Closes a specific Payment Link.
    # Args (provided by the tenant):
    #    payment_link_id (String, required): The ID of the Payment Link to close.
    # Returns:
    #    Response: A json object with the response value as well as other
    #    useful information such as status codes, headers and potential errors.

    # Prepare and execute response
    _path = f'/api/v1/payment_links/{payment_link_id}/cancel'
    _url = base_url + _path
    response = requests.put(_url, headers=headers)

    # deserialize and check errors
    decoded = json_deserialize(response.text)
    _result = check_errors(response, decoded)
    return _result


def send(headers, base_url, payment_link_id, obj):
    # Does a PUT request to /api/v1/payment_links/{payment_link_id}/distribute'.

    # Sends a Payment Link
    # Args (provided by the tenant):
    #    payment_link_id (String, required): The ID of the of the Payment Link.
    #    obj (json, required): json object containing information about how the payment link is getting distributed.
    #    To obtain the necessary information, use the documentation.
    # Returns:
    #    Response: A json object with the response value as well as other
    #    useful information such as status codes, headers and potential errors.

    # Prepare and execute response
    _path = f'/api/v1/payment_links/{payment_link_id}/distribute'
    _url = base_url + _path
    response = requests.put(_url, headers=headers, json=obj)

    # deserialize and check errors
    decoded = json_deserialize(response.text)
    _result = check_errors(response, decoded)
    return _result
