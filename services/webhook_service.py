from .twilio_service import TwilioService


class WebhookService:
    def __init__(self):
        self.twilio = TwilioService()

    def handle_webhook(self, data):
        event_type = data.get("EventType")

        if event_type == "onMessageAdded":
            if data.get("Body", "").lower() == "hello":
                self.twilio.send_conversation_reply(
                    data["ConversationSid"],
                    "Hello there! How can I help you today?"
                )
        return {"status": "success"}