import datetime

from util_salesforce import SalesforceJSON, Salesforce, SalesforceParser
from util_slack import BlockKit, Slack, SlackParser
from util import Util
from config import Config
import json
import threading


class HandleRequests:

    @staticmethod
    def post_buy_now(request):
        print(request.json)
        slack = Slack(Config.slack_bot_token)

        if SalesforceJSON.is_valid_request(request.json):
            channel_name = "fire-sale-" + str(Util.current_milli_time())
            sf_json = SalesforceJSON.parse_json(request.json)

            # Create New Channel
            channel_res = slack.create_private_channel(channel_name)
            channel_id = SlackParser.get_channel_id(channel_res)

            # Add Member to the Channel
            slack.add_member_to_channel(channel_id, [sf_json.slack_user_id])

            # Welcome message
            slack.post_message(channel_id,
                               "<@" + sf_json.slack_user_id + ">")

            blocks = HandleRequests.build_buy_now_message(sf_json)
            slack.post_block_message_to_channel(channel_id=channel_id,
                                                text="Deal", blocks=blocks)

    @staticmethod
    def payment_confirmation(request):
        req_json = request.json
        print(req_json)
        slack = Slack(Config.slack_bot_token)

        channel_id = req_json["channelId"]
        message = "Payment " + req_json["paymentNumber"] + " was successful"
        slack.post_message(channel_id, message)

    @staticmethod
    def handle_user_action(request):

        # If the request can't be verified from Slack, return verification failed
        if not Slack.verify_signing_secret(request):
            return BlockKit.slack_response_in_channel("Verification failed. Signature invalid.", False)

        req_json = json.loads(request.form['payload'])
        print(req_json)

        action = req_json["actions"][0]["value"]
        channel_id = req_json["channel"]["id"]
        response_url = req_json["response_url"]
        print(action)

        action_name = action.split("_")[0]
        fire_sale_id = action.split("_")[1]

        if action_name == "buynow":

            # Send reply to Slack
            data = HandleRequests.get_user_action_approve_message(req_json)
            res = Slack.post(response_url, json.dumps(data))
            print(res.json())

            # Buy Now in Background
            req_thread = threading.Thread(target=HandleRequests.buy_now_in_background,
                                          args=(
                                              fire_sale_id, channel_id))
            req_thread.daemon = False
            req_thread.start()
            return BlockKit.slack_response("")
        else:
            # Send reply to Slack
            data = HandleRequests.get_user_action_reject_message(req_json)
            res = Slack.post(response_url, json.dumps(data))
            print(res.json())

            return BlockKit.slack_response("Thank you")

    @staticmethod
    def build_buy_now_message(sf_json):
        blocks = []

        blocks.append(BlockKit.slack_mbuilder_section(
            "*This sale expires in 24 Hours! Act Now!* \n\n*" + sf_json.product_name + "*"))
        # header = ":flashing-siren: FLASH SALE :flashing-siren:\n\n*" + sf_json.product_name + "*"
        # blocks.append(BlockKit.slack_mbuilder_section(header))
        blocks.append(BlockKit.slack_mbuilder_divider())

        text = "*List Price:* $" + str(sf_json.list_price) + " \n*Quantity:* " + str(
            sf_json.quantity) + "\n*Discount:* " + str(sf_json.discount) + "% \n*Unit Price:* $" + str(
            sf_json.unit_price) + ""
        blocks.append(BlockKit.slack_mbuilder_section_accessory(text, sf_json.image_url))
        blocks.append(BlockKit.slack_mbuilder_divider())

        total_amount = "*Total Amount:* $" + str(sf_json.total_amount) + " / Month"
        blocks.append(BlockKit.slack_mbuilder_section(total_amount))

        elements = []
        elements.append(BlockKit.slack_mbuilder_action_element("Buy Now", "buynow_" + sf_json.fire_sale_id, "primary"))
        elements.append(BlockKit.slack_mbuilder_action_element("Cancel", "cancel_" + sf_json.fire_sale_id, "danger"))
        blocks.append(BlockKit.slack_mbuilder_action(elements))

        print(blocks)
        return blocks

    @staticmethod
    def get_user_action_approve_message(req_json):

        message_blocks = req_json["message"]["blocks"]
        slack_user_id = req_json["user"]["id"]
        # Remove Buttons from the message
        message_blocks.pop()

        message_blocks.append(
            BlockKit.slack_mbuilder_section(":white_check_mark: <@" + slack_user_id + "> approved the deal"))

        blocks = {"blocks": message_blocks}
        print(blocks)
        return blocks

    @staticmethod
    def get_user_action_reject_message(req_json):

        message_blocks = req_json["message"]["blocks"]
        slack_user_id = req_json["user"]["id"]
        # Remove Buttons from the message
        message_blocks.pop()

        message_blocks.append(
            BlockKit.slack_mbuilder_section(":negative_squared_cross_mark: <@" + slack_user_id + "> rejected the deal"))

        blocks = {"blocks": message_blocks}
        print(blocks)
        return blocks

    @staticmethod
    def buy_now_in_background(fire_sale_id, channel_id):
        salesforce = Salesforce(Config.sf_oauth_url, username=Config.sf_username, password=Config.sf_password,
                                security_token=Config.sf_security_token, client_id=Config.sf_client_id,
                                client_secret=Config.sf_client_secret)
        endpoint = Config.sf_org_url + Config.sf_fire_sale_buy_now_endpoint
        data = '{"inputs": [{"fireSaleId" : "' + fire_sale_id + '", "slackChannelId": "' + channel_id + '"}]}'
        headers = salesforce.get_headers()
        sf_res = salesforce.post(endpoint=endpoint, headers=headers, data=data)
        print(sf_res.json())

        slack = Slack(Config.slack_bot_token)
        if SalesforceParser.is_buy_now_success(sf_res.json()):
            order_number = SalesforceParser.get_order_number(sf_res.json())
            slack.post_message(channel_id, "Order " + order_number + " was created")
        else:
            slack.post_message(channel_id, "We couldn't create the order")
