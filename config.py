import os

class Config:
    sf_client_id = os.environ.get('SF_CLIENT_ID', None)
    sf_client_secret = os.environ.get('SF_CLIENT_SECRET', None)
    sf_org_url = os.environ.get('SF_ORG_URL', None)
    sf_oauth_url = os.environ.get('SF_OAUTH_URL', None)
    sf_username = os.environ.get('SF_USERNAME', None)
    sf_password = os.environ.get('SF_PASSWORD', None)
    sf_security_token = os.environ.get('SF_SECURITY_TOKEN', None)
    slack_bot_token = os.environ.get('SLACK_BOT_TOKEN', None)
    slack_user_token = os.environ.get('SLACK_USER_TOKEN', None)
    slack_signing_secret = os.environ.get('SLACK_SIGNING_SECRET', None)

    sf_fire_sale_buy_now_endpoint = os.environ.get('SF_FIRE_SALE_BUY_NOW_ENDPOINT', None)
