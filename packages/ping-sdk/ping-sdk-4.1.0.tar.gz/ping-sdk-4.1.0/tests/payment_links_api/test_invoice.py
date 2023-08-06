import uuid
import unittest
from dotenv import load_dotenv
from tests.payment_links_api.base_payment_links_api_test import BasePaymentLinksApiTest


class TestInvoice(BasePaymentLinksApiTest):

    def setUp(self):
        load_dotenv()
        super(TestInvoice, self).setUp()

# Get Invoice
    # get an invoice correctly(status code 200)

    def test_get_invoice_200(self):
        response = self.payment_links_api.invoice.get(self.payment_link_id)
        self.test_helper.run_tests(self, response)

    # error - gets an invoice with an incorrect id
    def test_get_invoice_id_not_found_404(self):
        response = self.payment_links_api.invoice.get(uuid.uuid4())
        self.test_helper.run_tests(self, response, 404)

    # error - gets a non existing invoice
    def test_get_invoice_no_existing_invoice_403(self):
        payment_link = self.payment_links_api.payment_link.create(self.complete_create_body)
        payment_link_id = payment_link.body["id"]
        response = self.payment_links_api.invoice.get(payment_link_id)
        self.test_helper.run_tests(self, response, 403)


# Create an invoice
    # Creates an invoice correctly (status code 200)

    def test_create_invoice_with_OCR_200(self):
        payment_link = self.payment_links_api.payment_link.create(self.complete_create_body)
        payment_link_id = payment_link.body["id"]
        response = self.payment_links_api.invoice.create(payment_link_id, {"reference_type": "OCR"})
        self.test_helper.run_tests(self, response, 204)


if __name__ == '__main__':
    unittest.main()
