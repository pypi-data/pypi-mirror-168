import unittest
import uuid
from dotenv import load_dotenv
from tests.payments_api.base_payments_api_test import BasePaymentsApiTest


class TestMerchant(BasePaymentsApiTest):

    def setUp(self):
        load_dotenv()
        super(TestMerchant, self).setUp()

# Get Merchants Tests
    # gets merchants successfully
    def test_list_200(self):
        response = self.payments_api.merchant.list()
        self.test_helper.run_tests(self, response)

# Create New Merchant Tests
    # creates a merchant correctly (status code 200)
    def test_create_200(self):
        response = self.payments_api.merchant.create(self.create_merchant_body)
        self.test_helper.run_tests(self, response)

# Get Specific Merchant Tests
    # get a specific merchant correctly (status code 200)
    def test_get_200(self):
        response = self.payments_api.merchant.get(self.merchant_id)
        self.test_helper.run_tests(self, response)

    # get a specific merchant with wrong id format (status code 422)
    def test_get_422(self):
        response = self.payments_api.merchant.get(0)
        self.test_helper.run_tests(self, response, 422)

    # get a specific merchant with a non-existing id (status code 404)
    def test_get_404(self):
        response = self.payments_api.merchant.get(uuid.uuid4())
        self.test_helper.run_tests(self, response, 404)


if __name__ == '__main__':
    unittest.main()
