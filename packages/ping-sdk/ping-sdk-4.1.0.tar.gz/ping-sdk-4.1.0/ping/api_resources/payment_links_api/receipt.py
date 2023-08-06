import requests
from ping.helper.apiHelper import check_errors, json_deserialize


def get(headers, base_url, payment_link_id):
    # Does a GET request to /api/v1/payment_links/{payment_link_id}/invoice.

    # Retrieves a specific Receipt.
    # Args (provided by the tenant):
    #    payment_link_id (String, required): The ID of the of the Payment Link from which you want a receipt.
    # Returns:
    #    Response: A json object with the response value as well as other
    #    useful information such as status codes, headers and potential errors.

    # Prepare and execute response
    _path = f'/api/v1/payment_links/{payment_link_id}/invoice'
    _url = base_url + _path
    response = requests.get(_url, headers=headers)

    # deserialize and check errors
    decoded = json_deserialize(response.text)
    _result = check_errors(response, decoded)
    return _result
