import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config import COLLECTION, logger
from typing import Optional, TypedDict, NotRequired, Literal
from datetime import datetime, timedelta


class Preferences(TypedDict):
    default_mode: Literal["brutal", "philosophical", "sarcastic"]
    share_as_image: NotRequired[bool]


class Subscription(TypedDict):
    plan: Literal["free", "premium"]
    expires_at: NotRequired[Optional[datetime]]


class Usage(TypedDict):
    messages_sent: int
    daily_limit: int
    last_reset: NotRequired[datetime]


class UserRecord(TypedDict):
    user_id: int
    username: str
    joined_at: datetime
    preferences: NotRequired[Preferences]
    subscription: Subscription
    usage: Usage
    last_message_time: NotRequired[Optional[datetime]]
    is_admin: NotRequired[bool]


class DataBase:
    def __init__(self):
        self.users = COLLECTION["users"]

    def register_user(
        self,
        user_id: int,
        username: str,
        response_mode: Optional[Literal["brutal","philosophical","sarcastic"]] = "brutal"
    ) -> bool:
        if self.users.find_one({"user_id": user_id}):
            logger.info(f"User {user_id} already in database.")
            return False

        new_user: UserRecord = {
            "user_id": user_id,
            "username": username,
            "joined_at": datetime.utcnow(),
            "preferences": {
                "default_mode": response_mode,
                "share_as_image": True
            },
            "subscription": {
                "plan": "free"
            },
            "usage": {
                "messages_sent": 0,
                "daily_limit": 10,
                "last_reset": datetime.utcnow()
            },
            "is_admin": False
        }

        self.users.insert_one(new_user)
        logger.info(f"User {user_id} added successfully.")
        return True

    def make_admin(self, user_id: int) -> bool:
        user = self.users.find_one({"user_id": user_id})
        if not user:
            logger.info(f"User {user_id} not found.")
            return False

        if user.get("is_admin", False):
            logger.info(f"User {user_id} already admin.")
            return True

        self.users.update_one(
            {"user_id": user_id},
            {"$set": {"is_admin": True}}
        )
        logger.info(f"User {user_id} promoted to admin.")
        return True

    def search_user(self, user_id: int) -> dict | bool:
        user = self.users.find_one({"user_id": user_id})
        if not user:
            logger.info(f"User {user_id} not found.")
            return False

        logger.info(f"Found user {user_id}")
        return user

    def is_admin(self, user_id: int) -> bool:
        return bool(
            self.users.find_one(
                {"user_id": user_id, "is_admin": True}
            )
        )

    def update_mode(
        self,
        user_id: int,
        mode: Literal["brutal","philosophical","sarcastic"]
    ) -> bool:
        result = self.users.update_one(
            {"user_id": user_id},
            {"$set": {"preferences.default_mode": mode}}
        )

        if result.matched_count == 0:
            logger.info(f"User {user_id} not found.")
            return False

        logger.info(f"User {user_id} mode updated to {mode}")
        return True

    def increment_message_count(self, user_id: int) -> bool:
        """Increment user's message count and reset if needed"""
        user = self.users.find_one({"user_id": user_id})
        
        if not user:
            logger.warning(f"User {user_id} not found.")
            return False

        usage = user.get("usage", {})
        last_reset = usage.get("last_reset", datetime.utcnow())
        current_time = datetime.utcnow()

        # Check if we need to reset daily count (24 hours passed)
        if (current_time - last_reset) > timedelta(days=1):
            # Reset the counter
            self.users.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "usage.messages_sent": 1,
                        "usage.last_reset": current_time,
                        "last_message_time": current_time
                    }
                }
            )
            logger.info(f"Reset daily counter for user {user_id}")
        else:
            # Just increment
            self.users.update_one(
                {"user_id": user_id},
                {
                    "$inc": {"usage.messages_sent": 1},
                    "$set": {"last_message_time": current_time}
                }
            )
            logger.info(f"Incremented message count for user {user_id}")

        return True

    def get_user_stats(self, user_id: int) -> dict | None:
        """Get user statistics"""
        user = self.users.find_one({"user_id": user_id})
        if not user:
            return None

        usage = user.get("usage", {})
        return {
            "messages_sent": usage.get("messages_sent", 0),
            "daily_limit": usage.get("daily_limit", 10),
            "remaining": usage.get("daily_limit", 10) - usage.get("messages_sent", 0),
            "plan": user.get("subscription", {}).get("plan", "free")
        }

    def upgrade_user_plan(self, user_id: int, plan: Literal["free", "premium"]) -> bool:
        """Upgrade or downgrade user plan"""
        user = self.users.find_one({"user_id": user_id})
        if not user:
            logger.warning(f"User {user_id} not found.")
            return False

        # Set new daily limits based on plan
        daily_limit = 100 if plan == "premium" else 10

        update_data = {
            "subscription.plan": plan,
            "usage.daily_limit": daily_limit
        }

        if plan == "premium":
            # Premium expires in 30 days
            update_data["subscription.expires_at"] = datetime.utcnow() + timedelta(days=30)
        else:
            update_data["subscription.expires_at"] = None

        self.users.update_one(
            {"user_id": user_id},
            {"$set": update_data}
        )

        logger.info(f"User {user_id} plan updated to {plan}")
        return True


if __name__ == "__main__":
    db = DataBase()
    