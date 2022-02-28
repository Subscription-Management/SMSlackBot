import os


class Config:
    sf_client_id = '3MVG9riCAn8HHkYUiHHef7FhIK0KS9ShEhbKiUaY7RfH07OSc2G2Y1iIaZH_ZWZhrB.nKVWCRgA=='
    sf_client_secret = 'BE797B897AA2CFB6E0BF67660BD5C671BE9B40DC354033F684DFBEBE2BBC059F'
    sf_org_url = 'https://demo-sm236-dev-org-dev-ed.my.salesforce.com'
    sf_oauth_url = 'https://login.salesforce.com/services/oauth2/token'
    sf_username = 'dgunaseelan@demo-sm236-dev.org'
    sf_password = 'salesforce1'
    sf_security_token = '0YZ18nKFCgu1jwJNEeo3T3dj7'
    slack_bot_token = 'xoxb-1787925222736-3178739842160-fEPej9lqvV7ZmeGRSBICMSkl'
    slack_user_token = 'xoxp-1787925222736-1776712058161-31483323x86262-dc2b4608804e970a1364e524554c8b61'
    slack_signing_secret = '5cabbab9cc9a867285c71de7988834ea'

    sf_fire_sale_buy_now_endpoint = "/services/data/v54.0/actions/custom/flow/Fire_Sale_Buy_Now"

# class Config:
#     sf_client_id = os.environ.get('SF_CLIENT_ID', None)
#     sf_client_secret = os.environ.get('SF_CLIENT_SECRET', None)
#     sf_org_url = os.environ.get('SF_ORG_URL', None)
#     sf_oauth_url = os.environ.get('SF_OAUTH_URL', None)
#     sf_username = os.environ.get('SF_USERNAME', None)
#     sf_password = os.environ.get('SF_PASSWORD', None)
#     sf_security_token = os.environ.get('SF_SECURITY_TOKEN', None)
#     slack_bot_token = os.environ.get('SLACK_BOT_TOKEN', None)
#     slack_user_token = os.environ.get('SLACK_USER_TOKEN', None)
#     slack_signing_secret = os.environ.get('SLACK_SIGNING_SECRET', None)
#
#     sf_fire_sale_buy_now_endpoint = os.environ.get('SF_FIRE_SALE_BUY_NOW_ENDPOINT', None)
