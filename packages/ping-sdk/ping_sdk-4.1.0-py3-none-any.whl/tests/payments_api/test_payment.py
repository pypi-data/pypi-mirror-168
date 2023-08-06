import unittest
import uuid
from dotenv import load_dotenv
from tests.payments_api.base_payments_api_test import BasePaymentsApiTest


class TestPayment(BasePaymentsApiTest):

    def setUp(self):
        load_dotenv()
        super(TestPayment, self).setUp()

# Get Payments Tests
    # gets payment correctly
    def test_get_payment_200(self):
        payment_id = self.create_payment_and_return_id(self.payment_order_id)
        self.await_payment_status_completed(self.payment_order_id, payment_id)

        response = self.payments_api.payment.get(self.payment_order_id, payment_id)
        self.test_helper.run_tests(self, response, 200)

    # gets payment with an incorrect id
    def test_get_payment_404(self):
        payment_id = ""
        response = self.payments_api.payment.get(self.payment_order_id, payment_id)
        self.test_helper.run_tests(self, response, 404)

# Initiate Payment Tests
    # Initiate a correct payment (status code 200)
    def test_initiate_payment_200(self):
        response = self.payments_api.payment.initiate(self.dummy_body, self.payment_order_id)
        self.test_helper.run_tests(self, response)

    # Initiate a payment with incorrect values inside payment object (status code 422)
    def test_initiate_payment_422(self):
        self.dummy_body["method"] = 0
        response = self.payments_api.payment.initiate(self.dummy_body, self.payment_order_id)
        self.test_helper.run_tests(self, response, 422)

    # Initiate a payment on a non-existing payment order (status code 404)
    def test_initiate_payment_404(self):
        response = self.payments_api.payment.initiate(self.dummy_body, uuid.uuid4())
        self.test_helper.run_tests(self, response, 404)


if __name__ == '__main__':
    unittest.main()
