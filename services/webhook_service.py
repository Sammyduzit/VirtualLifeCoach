"""
Webhook processing service for Twilio Conversation events.

Handles incoming webhook payloads and routes them to appropriate services.
"""
from .twilio_service import TwilioService
from pprint import pprint
import json
from get_EAN_by_product import get_matched_products
from nutrients_by_product import get_product_nutrients
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
        food_matches_dict = dict(load_file("food_matches.json"))
        #meal_nutrition = dict(load_file("meal_nutrition.json"))
        #daily_nutrition = dict(load_file("daily_nutrition.json"))
        #daily_nutrition = {date: {carbohydrates: 100, protein:100...}}

        message_data = data
        pprint(message_data)


        print("Conv sids: ",conversation_sids, type(conversation_sids))

        event_type = data.get("EventType")
        conversation_sid = data.get("ConversationSid")


        print("Conv SID: ",conversation_sid)

        if event_type == "onMessageAdded":
            #current_date = data.get('DateCreated') (without timestamp)
            #last_date = next(iter(daily_nutrition), None)
            # if current_date != last_date:
            #     daily_nutrition.clear()


            print("entered new message")
            print(user_data)
            print(user_data.get(conversation_sid, {}).get("Tracking_complete"))

            if not user_data.get(conversation_sid, {}).get("Tracking_complete"):
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
                    user_data[conversation_sid]["Tracking_complete"] = True
                    save_file("user_data.json", user_data)

            else:
                print("entered else")
                # if data.get("Body").strip().lower() == 'done':
                #     send_conv_reply(meal_nutrition)
                #     daily_nutrition = add meal nutrition
                #     save daily_nutrition
                #     send_conv_reply(daily_nutrition)
                #     meal_nutrition.clear()

                if not food_matches_dict:
                    food_input = data.get("Body").strip()

                    food_api_response = get_matched_products(food_input)

                    if len(food_api_response) > 1:
                        self.twilio.send_conversation_reply(
                            data["ConversationSid"],
                        "I have found multiple matches, which one is the closest to your product?\n"
                        )

                        # for index, key, value in enumerate(food_api_response):
                        #     food_matches_dict[index] = {key : value}
                        # food_matches_dict["1"] = food_api_response

                        for index, match in enumerate(food_api_response):
                            food_matches_dict[str(index + 1)] = {
                                "name": match["product_name"],
                                "code": match["code"]
                            }

                        # formatted_food_matches = "Here formatted food matches"
                        formatted_food_matches = "\n".join(
                            [f"{i + 1}. {match['product_name']} ({match['brands']})" for i, match in
                             enumerate(food_api_response)])

                        self.twilio.send_conversation_reply(
                            data["ConversationSid"], formatted_food_matches)

                        save_file("food_matches.json", food_matches_dict)
                        print("file saved")
                        matches_send = True
                        print("matches send true")
                else:
                    number_of_chosen_match = data.get("Body").strip()
                    number_of_chosen_match = int(number_of_chosen_match)
                    #match_name, match_code = food_matches_dict[number_of_chosen_match]

                    selected = food_matches_dict[str(number_of_chosen_match)]
                    food_api_nutrition_response = get_product_nutrients(selected["code"])

                    #nutrition_response = "Here formatted nutrition response." Check units!
                    nutrition_response = (f"{selected["name"]} - Calories: {food_api_nutrition_response["calories_100g"]} kcal,"
                                          f" Protein: {food_api_nutrition_response["proteins_100g"]}g")

                    # add to meal_nutrition
                    # save meal_nutrition
                    #Type 'done' if that's all for now, in message

                    self.twilio.send_conversation_reply(
                        data["ConversationSid"], nutrition_response
                    )

                    food_matches_dict.clear()
                    save_file("food_matches.json", food_matches_dict)




        return {"status": "success"}