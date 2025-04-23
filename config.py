"""
Configuration module for VirtualLifeCoach Twilio integration.

This module handles environment variables and provides centralized configuration
settings for the Twilio Conversations API.
"""

from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    """
    Container for Twilio configuration settings.

    Attributes:
        TWILIO_ACCOUNT_SID (str): Twilio account SID
        TWILIO_API_KEY_SID (str): Twilio API key SID
        TWILIO_API_KEY_SECRET (str): Twilio API key secret
        CONVERSATION_SERVICE_SID (str): Twilio Conversations service SID
    """
    TWILIO_ACCOUNT_SID = os.getenv("MS_TWILIO_ACCOUNT_SID")
    TWILIO_API_KEY_SID = os.getenv("MS_TWILIO_API_KEY_SID")
    TWILIO_API_KEY_SECRET = os.getenv("MS_TWILIO_API_KEY_SECRET")
    CONVERSATION_SERVICE_SID = os.getenv("CONVERSATION_SERVICE_SID")