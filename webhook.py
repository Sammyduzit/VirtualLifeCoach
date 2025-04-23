from flask import Flask, request, jsonify
from services.webhook_service import WebhookService

app = Flask(__name__)
webhook_service = WebhookService()

@app.route("/", methods=["GET"])
def home():
    return "Webhook server is running!"

@app.route("/conversations/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json if request.is_json else request.form.to_dict()
        result = webhook_service.handle_webhook(data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"status": "error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0")