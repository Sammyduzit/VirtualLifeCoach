"""
Webhook processing service for Twilio Conversation events.

Handles incoming webhook payloads and routes them to appropriate services.
"""

from .twilio_service import TwilioService


class WebhookService:
    """
    Orchestrates webhook event processing.
    """
    def __init__(self):
        """
        Initialize with Twilio service dependency.
        """
        self.twilio = TwilioService()


    def handle_webhook(self, data):
        """
        Process incoming webhook payload.
        :param data: (dict): Parsed webhook data containing:
                - EventType (str): Webhook event type
                - ConversationSid (str): Conversation identifier
                - Body (str): Optional message content
        :return: dict: Processing status dictionary
        """
        event_type = data.get("EventType")

        if event_type == "onMessageAdded":
            if data.get("Body", "").lower() == "hello":
                self.twilio.send_conversation_reply(
                    data["ConversationSid"],
                    "Hello there! How can I help you today?"
                )
        return {"status": "success"}