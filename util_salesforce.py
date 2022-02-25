import requests


class Salesforce:

    def __init__(self, oauth_endpoint, username, password, security_token, client_id, client_secret):
        data = {"username": username, "password": password + security_token, "client_id": client_id,
                "client_secret": client_secret, "grant_type": "password"}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        res = self.post(oauth_endpoint, headers, data)
        if res.status_code == 200:
            res_json = res.json()
            self.token = res_json["access_token"]
            print(self.token)
        else:
            raise Exception("Couldn't authenticate using OAuth: Endpoint returned status " + str(res.status_code))

    def get_headers(self):
        headers = {"Content-Type": "application/json", "Authorization": "Bearer " + self.token}
        return headers

    def post(self, endpoint, headers, data):
        res = requests.post(endpoint, data=data, headers=headers)
        return res


class SalesforceJSON:
    product_name: str
    list_price: float
    quantity: int
    discount: int
    unit_price: float
    total_amount: float
    pricebook_entry_id: str
    slack_user_id: str
    image_url: str

    @staticmethod
    def parse_json(req_json):
        sf_json = SalesforceJSON
        sf_json.product_name = req_json["productName"]
        sf_json.list_price = req_json["listPrice"]
        sf_json.quantity = req_json["quantity"]
        sf_json.discount = req_json["discount"]
        sf_json.unit_price = req_json["unitPrice"]
        sf_json.total_amount = req_json["totalAmount"]
        sf_json.pricebook_entry_id = req_json["priceBookEntryId"]
        sf_json.slack_user_id = req_json["slackUserId"]
        sf_json.image_url = req_json["imageUrl"]
        sf_json.fire_sale_id = req_json["fireSaleId"]

        return sf_json

    @staticmethod
    def is_valid_request(req_json):
        return "productName" in req_json


class SalesforceParser:

    @staticmethod
    def is_buy_now_success(res):
        return res[0]["isSuccess"]

    @staticmethod
    def get_order_number(res):
        return res[0]["outputValues"]["orderOutput"]["OrderNumber"]
