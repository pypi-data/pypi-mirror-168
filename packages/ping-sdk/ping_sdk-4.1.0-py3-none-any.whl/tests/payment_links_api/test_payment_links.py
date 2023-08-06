import unittest
import uuid
from dotenv import load_dotenv
from tests.payment_links_api.base_payment_links_api_test import BasePaymentLinksApiTest


class TestPaymentLinks(BasePaymentLinksApiTest):

    def setUp(self):
        load_dotenv()
        super(TestPaymentLinks, self).setUp()

# List Payment Links
    # lists all payment links correctly(status code 200)
    def test_list_payment_links_200(self):
        response = self.payment_links_api.payment_link.list()
        self.test_helper.run_tests(self, response, 200)

# Get Payment Link Tests
    # gets a payment link correctly
    def test_get_payment_link_200(self):
        response = self.payment_links_api.payment_link.get(self.payment_link_id)
        self.test_helper.run_tests(self, response, 200)

    # error - gets a payment link with an incorrect id
    def test_get_payment_link_404(self):
        response = self.payment_links_api.payment_link.get(uuid.uuid4())
        self.test_helper.run_tests(self, response, 404)

# Create Payment Link
    # Creates a payment link correctly (status code 200)
    def test_create_payment_link_200(self):
        response = self.payment_links_api.payment_link.create(self.complete_create_body)
        self.test_helper.run_tests(self, response)

    def test_create_payment_link_non_matching_total_amount_422(self):
        request = {
            "customer": self.customer,
            "items": self.items,
            "locale": "sv-SE",
            "payment_order_id": self.payment_order_id,
            "payment_provider_methods": self.swish_parameters,
            "supplier": self.supplier,
            "currency": "SEK",
            "total_amount": 0
        }
        response = self.payment_links_api.payment_link.create(request)
        self.test_helper.run_tests(self, response, 403)

    def test_create_payment_link_no_customer_422(self):
        request = {
            "items": self.items,
            "locale": "sv-SE",
            "payment_order_id": self.payment_order_id,
            "payment_provider_methods": self.swish_parameters,
            "supplier": self.supplier,
            "currency": "SEK",
            "total_amount": 14000
        }
        response = self.payment_links_api.payment_link.create(request)
        self.test_helper.run_tests(self, response, 422)

    def test_create_payment_link_no_items(self):
        request = {
            "customer": self.customer,
            "locale": "sv-SE",
            "payment_order_id": self.payment_order_id,
            "payment_provider_methods": self.swish_parameters,
            "supplier": self.supplier,
            "currency": "SEK",
            "total_amount": 0
        }
        response = self.payment_links_api.payment_link.create(request)
        self.test_helper.run_tests(self, response, 422)

    def test_create_payment_link_no_locale(self):
        request = {
            "customer": self.customer,
            "items": self.items,
            "payment_order_id": self.payment_order_id,
            "payment_provider_methods": self.swish_parameters,
            "supplier": self.supplier,
            "currency": "SEK",
            "total_amount": 14000
        }
        response = self.payment_links_api.payment_link.create(request)
        self.test_helper.run_tests(self, response, 422)

    def test_create_payment_link_no_id_422(self):
        request = {
            "customer": self.customer,
            "items": self.items,
            "locale": "sv-SE",
            "payment_provider_methods": self.swish_parameters,
            "supplier": self.supplier,
            "currency": "SEK",
            "total_amount": 14000
        }
        response = self.payment_links_api.payment_link.create(request)
        self.test_helper.run_tests(self, response, 422)

    def test_create_payment_link_id_not_found_403(self):
        request = {
            "customer": self.customer,
            "items": self.items,
            "locale": "sv-SE",
            "payment_order_id": str(uuid.uuid4()),
            "payment_provider_methods": self.swish_parameters,
            "supplier": self.supplier,
            "currency": "SEK",
            "total_amount": 14000
        }
        response = self.payment_links_api.payment_link.create(request)
        self.test_helper.run_tests(self, response, 403)

    def test_create_payment_link_no_provider_method_parameters_422(self):
        request = {
            "customer": self.customer,
            "items": self.items,
            "locale": "sv-SE",
            "payment_order_id": self.payment_order_id,
            "supplier": self.supplier,
            "currency": "SEK",
            "total_amount": 14000
        }
        response = self.payment_links_api.payment_link.create(request)
        self.test_helper.run_tests(self, response, 422)

    def test_create_payment_link_no_supplier_422(self):
        request = {
            "customer": self.customer,
            "items": self.items,
            "locale": "sv-SE",
            "payment_order_id": self.payment_order_id,
            "payment_provider_methods": self.swish_parameters,
            "currency": "SEK",
            "total_amount": 14000
        }
        response = self.payment_links_api.payment_link.create(request)
        self.test_helper.run_tests(self, response, 422)

    def test_create_payment_link_no_currency_422(self):
        request = {
            "customer": self.customer,
            "items": self.items,
            "locale": "sv-SE",
            "payment_order_id": self.payment_order_id,
            "payment_provider_methods": self.swish_parameters,
            "supplier": self.supplier,
            "total_amount": 14000
        }
        response = self.payment_links_api.payment_link.create(request)
        self.test_helper.run_tests(self, response, 422)

    def test_cancel_payment_link_204(self):
        payment_link = self.payment_links_api.payment_link.create(self.complete_create_body)
        payment_link_id = payment_link.body["id"]
        response = self.payment_links_api.payment_link.cancel(payment_link_id)
        self.test_helper.run_tests(self, response, 204)

    def test_cancel_payment_link_id_not_found_404(self):
        response = self.payment_links_api.payment_link.cancel(uuid.uuid4())
        self.test_helper.run_tests(self, response, 404)

    def test_cancel_payment_link_already_canceled_403(self):
        response = self.payment_links_api.payment_link.cancel(self.payment_link_id)
        self.test_helper.run_tests(self, response, 403)

    def test_send_payment_link_with_sms_204(self):
        request = {
            "methods": ["sms"],
            "customer_phone": "0701231212",
        }
        response = self.payment_links_api.payment_link.send(self.payment_link_id, request)
        self.test_helper.run_tests(self, response, 204)

    def test_send_payment_link_with_email_204(self):
        request = {
            "methods": ["email"],
            "customer_email": "somemail@mail.com",
        }
        response = self.payment_links_api.payment_link.send(self.payment_link_id, request)
        self.test_helper.run_tests(self, response, 204)

    def test_send_payment_link_with_sms_and_email_204(self):
        request = {
            "methods": ["sms", "email"],
            "customer_phone": "0701231212",
            "customer_email": "somemail@mail.com"
        }
        response = self.payment_links_api.payment_link.send(self.payment_link_id, request)
        self.test_helper.run_tests(self, response, 204)

    def test_send_payment_link_with_empty_request_422(self):
        response = self.payment_links_api.payment_link.send(self.payment_link_id, {})
        self.test_helper.run_tests(self, response, 422)

    def test_send_payment_link_id_not_found_404(self):
        response = self.payment_links_api.payment_link.send(uuid.uuid4(), {"methods": ["sms"]})
        self.test_helper.run_tests(self, response, 404)


if __name__ == '__main__':
    unittest.main()
