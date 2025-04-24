"""
Webhook processing service for Twilio Conversation events.

Handles incoming webhook payloads and routes them to appropriate services.
"""

from .twilio_service import TwilioService
from pprint import pprint
import json
import os


def load_file(filename):
    try:
        with open(filename, "r") as handle:
            data = json.load(handle)
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return ""


def save_file(filename, data):
    with open(filename, "w") as handle:
        json.dump(data, handle)



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
        conversation_sids = list((load_file("conversation_sids.json")))
        user_data = dict(load_file("user_data.json"))
        #json file für conv sids und json file for personal data
        message_data = data
        pprint(message_data)

        print("Conv sids: ",conversation_sids, type(conversation_sids))

        event_type = data.get("EventType")
        conversation_sid = data.get("ConversationSid")


        print("Conv SID: ",conversation_sid)

        if event_type == "onMessageAdded":

            print("entered checking")
            print(user_data)

            if not user_data.get(f'{conversation_sid}["Tracking complete"]'):
                if conversation_sid not in conversation_sids:
                    print("entered check for sid")
                    conversation_sids.append(conversation_sid)
                    print("append successful")
                    save_file("conversation_sids.json", conversation_sids)
                    user_data[conversation_sid] = {}
                    save_file("user_data.json",user_data)
                    self.twilio.send_conversation_reply(
                        data["ConversationSid"],
                        "Welcome to your personal Life Coach journey!\nHow should I call you?"
                    )


                elif not user_data[conversation_sid].get("Name"):
                    print("entered name check")
                    user_data[conversation_sid]["Name"] = data.get("Body")
                    save_file("user_data.json", user_data)
                    self.twilio.send_conversation_reply(
                        data["ConversationSid"],
                        "What is your age?"
                    )

                elif not user_data[conversation_sid].get("Age"):
                    user_data[conversation_sid]["Age"] = data.get("Body")
                    save_file("user_data.json", user_data)
                    self.twilio.send_conversation_reply(
                        data["ConversationSid"],
                        "How tall are you?"
                    )

                elif not user_data[conversation_sid].get("Height"):
                    user_data[conversation_sid]["Height"] = data.get("Body")
                    save_file("user_data.json", user_data)
                    self.twilio.send_conversation_reply(
                        data["ConversationSid"],
                        "How much do you weigh?"
                    )

                elif not user_data[conversation_sid].get("Weight"):
                    user_data[conversation_sid]["Weight"] = data.get("Body")
                    save_file("user_data.json", user_data)
                    self.twilio.send_conversation_reply(
                        data["ConversationSid"],
                        "What is your sex?"
                    )

                elif not user_data[conversation_sid].get("Sex"):
                    user_data[conversation_sid]["Sex"] = data.get("Body")
                    save_file("user_data.json", user_data)
                    self.twilio.send_conversation_reply(
                        data["ConversationSid"],
                        "What is your diet?"
                    )

                elif not user_data[conversation_sid].get("Diet"):
                    user_data[conversation_sid]["Diet"] = data.get("Body")
                    save_file("user_data.json", user_data)
                    self.twilio.send_conversation_reply(
                        data["ConversationSid"],
                        "What are your daily activities?"
                    )

                elif not user_data[conversation_sid].get("Daily_Activity"):
                    user_data[conversation_sid]["Daily_Activity"] = data.get("Body")
                    save_file("user_data.json", user_data)
                    self.twilio.send_conversation_reply(
                        data["ConversationSid"],
                        "What is your goal?"
                    )


                elif not user_data[conversation_sid].get("Goal"):
                    user_data[conversation_sid]["Goal"] = data.get("Body")
                    self.twilio.send_conversation_reply(
                        data["ConversationSid"],
                        "Please enter your meal, each ingredient one by one"
                    )
                    user_data[conversation_sid]["Tracking complete"] = True
                    save_file("user_data.json", user_data)

            else:
                pass #body als string zu nicolas

        return {"status": "success"}