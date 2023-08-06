from requests import get, post


class Payment:

    def __init__(self, amount, currency, description, url, code, headers):
        self.amount = amount
        self.currency = currency
        self.description = description
        self.url = url
        self.code = code
        self.headers = headers
        self.api_url = 'https://api.commerce.coinbase.com/charges/' + code

    def is_paid(self) -> bool:
        r = get(self.api_url, headers=self.headers)
        for i in r.json()['data']['timeline']:
            if i['status'] == 'COMPLETED':
                return True


class CoinbaseAPI(object):

    def __init__(self, api_key: str) -> None:
        """
        Initialize the API
        :param api_key:
        """
        self.api_key = api_key
        self.url = "https://api.commerce.coinbase.com/"
        self.headers = {"X-CC-Api-Key": self.api_key, "X-CC-Version": "2018-03-22"}
        self.check()

    def check(self) -> None:
        r = get(self.url + "checkouts", headers=self.headers).status_code
        if r == 401:
            raise AuthError("Invalid CoinBase API Key")
        elif r == 429:
            raise AuthError("Rate limit exceeded")
        elif r == 500 or r == 503:
            raise AuthError("CoinBase API is down")

    def create_charge(self, title: str, description: str, price: float, currency: str) -> Payment:

        """
        Create charge (invoice) on coinbase
        :param title: Title of the charge
        :param description: Description of the charge
        :param price: Price of the charge
        :param currency: Currency of the charge
        :return:
        """

        self.headers["Content-Type"] = "application/json"
        self.headers["Accept"] = "application/json"
        data = {
            "name": title,
            "description": description,
            "local_price": {"amount": price, "currency": currency},
            "pricing_type": "fixed_price"
        }
        r = post(self.url + "charges", headers=self.headers, json=data).json()
        return Payment(price, currency, description, r["data"]["hosted_url"], r["data"]["code"], self.headers)


class AuthError(Exception):
    pass