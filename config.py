from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    TWILIO_ACCOUNT_SID = os.getenv("MS_TWILIO_ACCOUNT_SID")
    TWILIO_API_KEY_SID = os.getenv("MS_TWILIO_API_KEY_SID")
    TWILIO_API_KEY_SECRET = os.getenv("MS_TWILIO_API_KEY_SECRET")
    CONVERSATION_SERVICE_SID = os.getenv("CONVERSATION_SERVICE_SID")