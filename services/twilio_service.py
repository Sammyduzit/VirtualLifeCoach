"""
Twilio service layer for conversation message handling.
Provides functionality to send messages through Twilio's Conversations API.
"""
from twilio.rest import Client
from Projects.VirtualLifeCoach.config import Config

class TwilioService:
    """
    Handles all Twilio API communications.
    """
    def __init__(self):
        """
        Initialize Twilio client with configuration.
        """
        self.client = Client(
            Config.TWILIO_API_KEY_SID,
            Config.TWILIO_API_KEY_SECRET,
            Config.TWILIO_ACCOUNT_SID
        )

    def send_conversation_reply(self, conversation_sid, message):
        """
        Send a message to an existing Twilio conversation.
        :param conversation_sid: SID of target conversation
        :param message: Message content to send
        :return: Message SID if successful, None otherwise
        """
        try:
            reply_message = self.client.conversations.v1.services(
                Config.CONVERSATION_SERVICE_SID
            ).conversations(conversation_sid).messages.create(
                author="system",
                body=message
            )
            return reply_message.sid
        except Exception as e:
            print(f"Twilio error: {e}")
            return None