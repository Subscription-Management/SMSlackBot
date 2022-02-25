from slack_sdk import WebClient
from config import Config
import hashlib
import hmac
import requests


class Slack:

    def __init__(self, token):
        self.client = WebClient(token=token)

    def create_public_channel(self, channel_name):
        result = self.client.conversations_create(name=channel_name, is_private=False)
        print(result)
        return result

    def create_private_channel(self, channel_name):
        result = self.client.conversations_create(name=channel_name, is_private=True)
        print(result)
        return result

    def post_message(self, channel_id, message):
        result = self.client.chat_postMessage(channel=channel_id, text=message, link_names=True)
        print(result)
        return result

    def post_ephemeral_message(self, channel_id, user_id, message):
        result = self.client.chat_postEphemeral(channel=channel_id, user=user_id, text=message, link_names=True)
        print(result)
        return result

    def post_block_message_to_channel(self, channel_id, blocks, text):
        result = self.client.chat_postMessage(channel=channel_id, text=text, blocks=blocks, link_names=True)
        print(result)
        return result

    def post_ephemeral_message_to_channel(self, channel_id, user_id, message):
        result = self.client.chat_postEphemeral(channel=channel_id, user=user_id, text=message, link_names=True)
        print(result)
        return result

    def post_ephemeral_block_message_to_channel(self, channel_id, user_id, message, blocks):
        result = self.client.chat_postEphemeral(channel=channel_id, user=user_id, text=message, blocks=blocks,
                                                link_names=True)
        print(result)
        return result

    def add_member_to_channel(self, channel_id, user_list):
        result = self.client.conversations_invite(channel=channel_id, users=user_list)
        print(result)
        return result

    def pin_message_to_channel(self, channel_id, message_timestamp):
        result = self.client.pins_add(channel=channel_id, timestamp=message_timestamp)
        print(result)
        return result

    @staticmethod
    def verify_signing_secret(request):

        timestamp = request.headers['X-Slack-Request-Timestamp']
        request_body = request.get_data().decode('utf-8')
        slack_signature = request.headers['X-Slack-Signature']

        sig_basestring = 'v0:' + timestamp + ':' + request_body
        slack_signing_secret = Config.slack_signing_secret

        my_signature = "v0=" + hmac.new(slack_signing_secret.encode('utf-8'), msg=sig_basestring.encode('utf-8'),
                                        digestmod=hashlib.sha256).hexdigest()
        if hmac.compare_digest(my_signature, slack_signature):
            return True
        else:
            print("Verification failed. Signature invalid.")
            return False

    @staticmethod
    def post(endpoint, data):
        res = requests.post(endpoint, data=data, headers={"Content-Type": "application/json"})
        return res


class BlockKit:

    @staticmethod
    def slack_mbuilder_divider():
        return {"type": "divider"}

    @staticmethod
    def slack_mbuilder_section(text):
        return {"type": "section", "text": {"type": "mrkdwn", "text": text}}

    @staticmethod
    def slack_mbuilder_section_accessory(text, image_url):
        return {"type": "section", "text": {"type": "mrkdwn", "text": text},
                "accessory": {"type": "image", "image_url": image_url, "alt_text": "Product Image"}}

    @staticmethod
    def slack_mbuilder_action_element(text, value, style):
        return {"type": "button", "text": {"type": "plain_text", "emoji": True, "text": text}, "style": style,
                "value": value}

    @staticmethod
    def slack_mbuilder_action(elements):
        return {"type": "actions", "elements": elements}

    @staticmethod
    def slack_response_in_channel(response_text, replace_original):
        return {"response_type": 'in_channel', "text": response_text, "replace_original": replace_original}

    @staticmethod
    def slack_response(response_text):
        return {"response_type": "ephemeral", "text": response_text}


class SlackParser:

    @staticmethod
    def get_channel_id(channel_res):
        return channel_res['channel']['id']
