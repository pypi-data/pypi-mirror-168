import unittest
import uuid
from dotenv import load_dotenv
from tests.payment_links_api.base_payment_links_api_test import BasePaymentLinksApiTest


class TestReceipt(BasePaymentLinksApiTest):

    def setUp(self):
        load_dotenv()
        super(TestReceipt, self).setUp()

# Get Receipt
    # get an receipt correctly(status code 200)
    def test_get_receipt_200(self):
        response = self.payment_links_api.invoice.get(self.payment_link_id)
        self.test_helper.run_tests(self, response)

    # error - gets an receipt with an incorrect id
    def test_get_receipt_id_not_found_404(self):
        response = self.payment_links_api.invoice.get(uuid.uuid4())
        self.test_helper.run_tests(self, response, 404)

    # error - gets a receipt with an unfinished payment link
    def test_get_receipt_not_completed_403(self):
        payment_link = self.payment_links_api.payment_link.create(self.complete_create_body)
        payment_link_id = payment_link.body["id"]
        response = self.payment_links_api.invoice.get(payment_link_id)
        self.test_helper.run_tests(self, response, 403)


if __name__ == '__main__':
    unittest.main()
