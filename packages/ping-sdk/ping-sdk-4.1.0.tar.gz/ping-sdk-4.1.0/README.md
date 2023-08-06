# Ping Payments Python SDK

[![Tests](https://github.com/youcal/ping_python_sdk/actions/workflows/tests.yml/badge.svg)](https://github.com/youcal/ping_python_sdk/actions/workflows/tests.yml)
[![PyPI version](https://badge.fury.io/py/ping-sdk.svg)](https://badge.fury.io/py/ping-sdk)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

The Ping Payments Python SDK manages the [Ping Payments API](#payments-api) and [Ping Payment Links API](#payments-api).

## Table of contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Documentation](#documentation)
- [Ping Payments API](#payments-api)
- [Ping Payment Links API](#payments-api)
- [Usage](#usage)

## Requirements

The Ping Payments Python SDK supports the following versions of Python:

- Python 3, versions 3.7 and later

## Installation

Install the latest Ping Payments Python SDK using pip:

```sh
pip install ping-sdk
```

## Documentation

The Ping Payments Python SDK documentation contains complete information to be able to work with the SDK. Go to [Python SDK documentation](https://docs.pingpayments.com/docs/the-ping-payments-python-sdk) for the full documentation.

## [Ping Payments API]

The Ping Payments API is implemented as the `PaymentsApi` class contains a number of endpoints.

**Ping Payments API Endpoints**

- [Merchant]
- [Payment Orders]
- [Payment]
- [Payout]
- [Ping]

## [Ping Payment Links API]

The Ping Payments API is implemented as the `PaymentLinksApi` contains a number of endpoints.

**Ping Payment Links API Endpoints**

- [Payment Link]
- [Invoice]
- [Receipt]

## Usage

#### Get a tenant ID

Ping Payments provides you with a `tenant ID` and are used for resource permissions.

**Important:** Make sure you store and access the tenant ID securely.

#### Instructions

1. Import the PaymentsApi class from the Ping module:

```python
from ping.payments_api import PaymentsApi
```

2. Instantiate a PaymentsApi object and initialize it with the tenant ID and the environment that you want to use.

Initialize the PaymentsApi in production mode:

```python
payments_api = PaymentsApi(
		tenant_id = '55555555-5555-5555-5555-555555555555'
)
```

Initialize the PaymentsApi in sandbox mode, for testing:

```python
payments_api = PaymentsApi(
		tenant_id = '55555555-5555-5555-5555-555555555555',
		environment = 'sandbox'
)
```

#### Make calls

**Work with the API by by choosing a Endpoint and calling it´s methods.** For example, you can choose the endpoint `merchants` and call the method `list()` to a list of all merchants connected to a tenant:

```python
result = payments_api.merchant.list()
```

#### Handle the response

Calls to the Ping Payments API endpoint methods returns an ApiResponse object. Properties of the ApiResponse object contains information regarding request _(headers and request)_ and the response _(status_code, reason_phrase, text, errors, body, and cursor)_.

**Using the response:**

Check whether the response succeeded or failed. Two helper methods `is_success()`and `is_error()` in the ApiResponse object determine the success or failure of a call:

```python
if result.is_success():
	# Display the successful response as text
	print(result.text)
elif result.is_error():
	# Display the error response
	print(f"Errors: {result.errors}")
```

[//]: # "Link anchor definitions"
[ping payments api]: https://docs.pingpayments.com/docs/payments-api-1
[ping payment links api]: https://docs.pingpayments.com/docs/payment-links-api-1
[merchant]: https://docs.pingpayments.com/docs/payments-api-1#endpoint
[payment orders]: https://docs.pingpayments.com/docs/payments-api-1#endpoint-1
[payment]: https://docs.pingpayments.com/docs/payments-api-1#payment--endpoint
[payout]: https://docs.pingpayments.com/docs/payments-api-1#payout-endpoint
[ping]: https://docs.pingpayments.com/docs/verify-api-connection
[payment link]: https://docs.pingpayments.com/docs/payment-links-api-1#endpoint
[invoice]: https://docs.pingpayments.com/docs/payment-links-api-1#endpoint-1
[receipt]: https://docs.pingpayments.com/docs/payment-links-api-1#endpoint-2
