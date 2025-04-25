"""
Webhook processing service for Twilio Conversation events.

Handles incoming webhook payloads and routes them to appropriate services.
"""
import json
import os
import logging
from pprint import pprint

from .twilio_service import TwilioService
from .get_EAN_by_product import get_matched_products
from .nutrients_by_product import get_product_nutrients

logger = logging.getLogger(__name__)


# ⬅️ CHANGED: renamed from load_file, now returns a sensible default
def load_json(filename, default):
    try:
        with open(filename, "r") as handle:
            return json.load(handle)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


# ⬅️ CHANGED: renamed from save_file, now writes with indent for readability
def save_json(filename, data):
    with open(filename, "w") as handle:
        json.dump(data, handle, indent=2)


class WebhookService:
    """
    Orchestrates webhook event processing.
    """
    def __init__(self):
        self.twilio     = TwilioService()
        self.conv_file  = "conversation_sids.json"
        self.user_file  = "user_data.json"
        self.match_file = "food_matches.json"

    def handle_webhook(self, data):
        """
        Process incoming webhook payload.
        """
        pprint(data)
        event_type = data.get("EventType")
        sid        = data.get("ConversationSid")
        body       = data.get("Body", "").strip()

        if event_type != "onMessageAdded" or not sid:
            return {"status": "ignored"}

        # ⬅️ CHANGED: use load_json with defaults
        conversation_sids = load_json(self.conv_file, [])
        user_data         = load_json(self.user_file, {})
        matches_dict      = load_json(self.match_file, {})

        if sid not in conversation_sids:
            conversation_sids.append(sid)
            save_json(self.conv_file, conversation_sids)
            user_data[sid] = {}
            save_json(self.user_file, user_data)

        user = user_data.setdefault(sid, {})

        # ... (onboarding logic unchanged) ...

        if user.get("Tracking_complete"):

            # —— Stage 1: lookup with error handling —— #
            if not matches_dict:
                try:
                    api_matches = get_matched_products(body)
                    if not isinstance(api_matches, list) or not api_matches:
                        raise ValueError("No matches returned")
                except Exception:
                    logger.exception("Error fetching product matches")  # ⬅️ CHANGED
                    self.twilio.send_conversation_reply(
                        sid,
                        "Sorry, I couldn't find any products right now. Please try again later."
                    )
                    return {"status": "error"}

                # ⬅️ CHANGED: build selection list with only name + code
                formatted = []
                for idx, item in enumerate(api_matches, start=1):
                    name = item.get("product_name") or "Unknown product"
                    code = item.get("code")
                    if not code:
                        continue
                    matches_dict[str(idx)] = {"name": name, "code": code}
                    formatted.append(f"{idx}. {name} (code: {code})")

                if not formatted:
                    self.twilio.send_conversation_reply(
                        sid,
                        "I found products, but none had valid codes. Please try a different query."
                    )
                    return {"status": "error"}

                save_json(self.match_file, matches_dict)
                self.twilio.send_conversation_reply(
                    sid,
                    "I found multiple matches, please choose one:\n" + "\n".join(formatted)
                )
                return {"status": "awaiting_selection"}

            # —— Stage 2: selection & nutrition with error handling —— #
            choice = body
            if choice not in matches_dict:
                self.twilio.send_conversation_reply(
                    sid,
                    f"Please reply with a number between 1 and {len(matches_dict)}."
                )
                return {"status": "awaiting_valid_number"}

            selected = matches_dict[choice]
            name     = selected["name"]
            code     = selected["code"]

            # ⬅️ CHANGED: clear matches via save_json rather than os.remove
            save_json(self.match_file, {})

            # ⬅️ CHANGED: expanded fields + try/except around get_product_nutrients
            try:
                nutrients      = get_product_nutrients(code)
                calories       = nutrients.get("energy-kcal_100g", "Not available")
                carbohydrates  = nutrients.get("carbohydrates_100g", "Not available")
                fat            = nutrients.get("fat_100g", "Not available")
                sugars         = nutrients.get("sugars_100g", "Not available")
                salt           = nutrients.get("salt_100g", "Not available")
                proteins       = nutrients.get("proteins_100g", "Not available")

                # ⬅️ CHANGED: validate critical fields
                if calories == "Not available" or proteins == "Not available":
                    raise KeyError("Missing critical nutrition fields")
            except Exception:
                logger.exception("Error fetching nutrition data")
                self.twilio.send_conversation_reply(
                    sid,
                    f"Sorry, I couldn’t retrieve nutrition info for {name}. Please try another item."
                )
                return {"status": "error"}

            # ⬅️ CHANGED: full summary with all nutrients
            msg = (
                f"{name} — Calories: {calories} kcal, Carbohydrates: {carbohydrates} g, "
                f"Fat: {fat} g, Sugars: {sugars} g, Salt: {salt} g, Protein: {proteins} g"
            )
            self.twilio.send_conversation_reply(sid, msg)
            return {"status": "success"}

        return {"status": "success"}
