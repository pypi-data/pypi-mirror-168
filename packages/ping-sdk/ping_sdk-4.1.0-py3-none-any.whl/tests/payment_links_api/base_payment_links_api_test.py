import unittest
import os
import random
from faker import Faker
from tests.test_helper import TestHelper
from ping.payment_links_api import PaymentLinksApi

fake = Faker(['no_NO', 'sv_SE', 'en_US'])


class BasePaymentLinksApiTest(unittest.TestCase):

    def setUp(self):
        self.test_helper = TestHelper
        self.payment_links_api = PaymentLinksApi(os.getenv("TENANT_ID"))
        self.merchant_id = os.getenv("MERCHANT_ID")
        self.payment_link_id = os.getenv("PAYMENT_LINK_ID")
        self.payment_order_id = os.getenv("PAYMENT_ORDER_ID")

        self.customer = {
            "email": fake.free_email(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "phone": fake.phone_number()
        }
        self.items = [
            {
                "description": random.choice(["Hawaii Pizza", "Margarita", "Vesuvio", "Altono"]),
                "merchant_id": self.merchant_id,
                "price": random.choice([1000, 3500, 4000, 4500]),
                "quantity": random.randint(1, 5),
                "vat": random.choice([0, 6, 12, 25])
            }
        ]
        self.supplier = {
            "city": fake.city(),
            "name": fake.company(),
            "organization_number": str(random.randint(0000000000, 9999999999)),
            "website": fake.domain_name(),
            "zip": str(random.randint(00000, 99999))
        }
        self.swish_parameters = [
            {
                "method": "e_commerce",
                "parameters": {
                    "swish_message": "Pizza from the pizzeria"
                },
                "provider": "swish"
            }
        ]
        self.complete_create_body = {
            "customer": self.customer,
            "items": self.items,
            "locale": "sv-SE",
            "payment_order_id": self.payment_order_id,
            "payment_provider_methods": self.swish_parameters,
            "supplier": self.supplier,
            "currency": "SEK",
            "total_amount": int(self.items[0]["price"]) * int(self.items[0]["quantity"])
        }
