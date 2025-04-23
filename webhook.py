"""
Flask webhook endpoint controller for VirtualLifeCoach.

Provides HTTP endpoints for Twilio Conversation webhooks and handles request/response
cycles.
"""

from flask import Flask, request, jsonify
from services.webhook_service import WebhookService


app = Flask(__name__)
webhook_service = WebhookService()


@app.route("/", methods=["GET"])
def home():
    """
    Health check endpoint.
    :return: Service status message
    """
    return "Webhook server is running!"


@app.route("/conversations/webhook", methods=["POST"])
def webhook():
    """
    Primary webhook handler for Twilio Conversation events.
    :return: tuple: (response_dict, status_code)
    """
    try:
        data = request.json if request.is_json else request.form.to_dict()
        result = webhook_service.handle_webhook(data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"status": "error"}), 500


if __name__ == "__main__":
    """Run development server."""
    app.run(host="0.0.0.0", port=5000)