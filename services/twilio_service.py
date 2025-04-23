from twilio.rest import Client
from Projects.VirtualLifeCoach.config import Config

class TwilioService:
    def __init__(self):
        self.client = Client(
            Config.TWILIO_API_KEY_SID,
            Config.TWILIO_API_KEY_SECRET,
            Config.TWILIO_ACCOUNT_SID
        )

    def send_conversation_reply(self, conversation_sid, message):
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