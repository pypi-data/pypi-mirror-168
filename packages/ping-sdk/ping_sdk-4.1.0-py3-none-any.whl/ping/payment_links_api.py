from ping.api_resources.payment_links_api import payment_links
from ping.api_resources.payment_links_api import invoice
from ping.api_resources.payment_links_api import receipt
from ping.api_resources.payment_links_api import pings
from ping.helper.apiHelper import get_base_url


class PaymentLinksApi:
    # A controller to access all endpoints in the API.
    def __init__(self, tenant_id="", environment="sandbox"):
        self.tenant_id = tenant_id
        self.environment = environment
        self.base_url = get_base_url("payment_links_api", environment)
        self.headers = {
            "Accept": "application/json",
            "tenant_id": tenant_id
        }

    @property
    def payment_link(self):
        return Payment_link(self.headers, self.base_url)

    @property
    def invoice(self):
        return Invoice(self.headers, self.base_url)

    @property
    def receipt(self):
        return Receipt(self.headers, self.base_url)

    @property
    def ping(self):
        return Ping(self.headers, self.base_url)


class BaseEndpoints:
    # Endpoint classes inherit from this base class
    def __init__(self, headers, base_url):
        self.headers = headers
        self.base_url = base_url


class Payment_link(BaseEndpoints):
    # Endpoint class for Payment Links endpoints
    def list(self):
        return payment_links.list(self.headers, self.base_url)

    def create(self, obj):
        return payment_links.create(self.headers, self.base_url, obj)

    def get(self, payment_link_id):
        return payment_links.get(self.headers, self.base_url, payment_link_id)

    def cancel(self, payment_link_id):
        return payment_links.cancel(self.headers, self.base_url, payment_link_id)

    def send(self, payment_order_id, obj):
        return payment_links.send(self.headers, self.base_url, payment_order_id, obj)


class Invoice(BaseEndpoints):
    # Endpoint class for Invoice endpoints
    def create(self, payment_link_id, obj):
        return invoice.create(self.headers, self.base_url, payment_link_id, obj)

    def get(self, payment_link_id):
        return invoice.get(self.headers, self.base_url, payment_link_id)


class Receipt(BaseEndpoints):
    # Endpoint class for Receipt endpoints

    def get(self, payment_link_id):
        return receipt.get(self.headers, self.base_url, payment_link_id)


class Ping(BaseEndpoints):
    # Endpoint class for ping endpoints
    def ping_the_api(self):
        return pings.ping_the_api(self.headers, self.base_url)
