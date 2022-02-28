from flask import abort, Flask, jsonify, request
from app_handle_requests import HandleRequests

app = Flask(__name__)


# This endpoint is used from the Salesforce org
# to post buy-now message to the user in Slack
@app.route('/post_buy_now', methods=['POST'])
def post_buy_now():
    HandleRequests.post_buy_now(request)
    return jsonify(success=True)


@app.route('/handle_user_action', methods=['POST'])
def handle_user_action():
    return HandleRequests.handle_user_action(request)


@app.route('/payment_confirmation', methods=['POST'])
def handle_user_action():
    return HandleRequests.payment_confirmation(request)


if __name__ == '__main__':
    app.run()
