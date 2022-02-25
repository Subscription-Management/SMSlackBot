from util_salesforce import Salesforce
from config import Config
from util_slack import Slack

salesforce = Salesforce(oauth_endpoint=Config.sf_oauth_url, username=Config.sf_username, password=Config.sf_password,
                        security_token=Config.sf_security_token, client_id=Config.sf_client_id,
                        client_secret=Config.sf_client_secret)

slack = Slack(Config.slack_bot_token)
slack.post_message("U01NULY1Q4R", "Hello! How are you?")
