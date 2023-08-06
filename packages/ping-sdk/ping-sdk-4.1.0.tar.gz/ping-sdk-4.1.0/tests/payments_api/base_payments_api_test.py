import unittest
import os
import random
from faker import Faker
from tests.test_helper import TestHelper
from ping.payments_api import PaymentsApi

fake = Faker(['no_NO', 'sv_SE', 'en_US'])


class BasePaymentsApiTest(unittest.TestCase):

    def setUp(self):
        self.test_helper = TestHelper
        self.payments_api = PaymentsApi(os.getenv("TENANT_ID"))
        self.merchant_id = os.getenv("MERCHANT_ID")
        self.split_tree_id = os.getenv("SPLIT_TREE_ID")
        self.payment_id = os.getenv("PAYMENT_ID")
        self.payment_order_id = os.getenv("PAYMENT_ORDER_ID")

        self.dummy_body = {
            "currency": "SEK",
            "metadata": {
                "delivery_id": str(random.randint(00000, 99999))
            },
            "method": "dummy",
            "order_items": [
                {
                    "amount": 2500,
                    "merchant_id": self.merchant_id,
                    "name": "Delivery, Marios Pasta (Pasta La Vista)",
                    "vat_rate": random.choice([0, 6, 12, 25])
                },
            ],
            "provider": "dummy",
            "provider_method_parameters": {
                "desired_payment_status": "COMPLETED"
            },
            "total_amount": 2500
        }
        self.create_merchant_body = {
            "name": fake.company(),
            "organization":
                random.choice
                ([
                    {"country": "SE", "se_organization_number": str(random.randint(1000000000, 9999999999))},
                    {"country": "NO", "no_organization_number": str(random.randint(100000000, 999999999))}
                ])
        }

    def await_payment_status_completed(self, payment_order_id, payment_id):
        is_completed = False
        while not is_completed:
            payment = self.payments_api.payment.get(payment_order_id, payment_id)
            if payment.is_success():
                if payment.body["status"] == "COMPLETED":
                    is_completed = True
            else:
                break

    def create_payment_order_and_return_id(self):
        payment_order = self.payments_api.paymentOrder.create(self.split_tree_id, "SEK")
        return payment_order.body["id"]

    def create_payment_and_return_id(self, payment_order_id):
        payment_response = self.payments_api.payment.initiate(self.dummy_body, payment_order_id)
        return payment_response.body["id"]
