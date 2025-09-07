from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime
import pytz
from config import MONGO_URI
from utils.logger import logger

try:
    client = MongoClient(MONGO_URI)
    db = client["telegram_bot_db"]
    users_collection = db["users"]
    accounts_collection = db["accounts"]
    capacity_collection = db["capacity"]
    admin2fa_collection = db["admin2fa"]
    withdraw_collection = db["withdrawals"]
    settings_collection = db["settings"]  # ✅ support/channel info
    logger.info("MongoDB successfully connected.")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    exit()


# ------------------ User functions ------------------
def get_user_data(user_id: int):
    return users_collection.find_one({"user_id": user_id})


def create_user_data(user_id: int):
    user_data = {
        "user_id": user_id,
        "total_balance": 0.0,
        "verified_accounts_count": 0,
        "unverified_accounts_count": 0,
        "join_date": datetime.now(pytz.utc)
    }
    users_collection.insert_one(user_data)
    return user_data


def add_user_balance(user_id: int, amount: float):
    users_collection.update_one(
        {"user_id": user_id},
        {"$inc": {"total_balance": amount}}
    )


# ------------------ RESET BALANCES ------------------
def reset_all_balances():
    """সকল ইউজার এবং অ্যাকাউন্টের ব্যালেন্স 0 করে দিবে"""
    users_collection.update_many({}, {"$set": {"total_balance": 0}})
    accounts_collection.update_many({}, {"$set": {"balance": 0}})
    logger.info("✅ All balances have been reset to 0")
    return True


# ------------------ Capacity functions ------------------
def update_capacity_info(country_code: str, capacity: int, price: float, unlock_time: int):
    return capacity_collection.update_one(
        {"country_code": country_code},
        {"$set": {"capacity": capacity, "price": price, "unlock_time": unlock_time}}
    )


def delete_capacity_by_id(item_id: str):
    try:
        object_id = ObjectId(item_id)
        result = capacity_collection.delete_one({"_id": object_id})
        return result.deleted_count == 1
    except Exception as e:
        print(f"Error deleting capacity: {e}")
        return False


def insert_capacity_info(country_code: str, capacity: int, price: float, unlock_time: int):
    return capacity_collection.insert_one({
        "country_code": country_code,
        "capacity": capacity,
        "price": price,
        "unlock_time": unlock_time
    })


def get_capacity_data():
    return list(capacity_collection.find())


def update_capacity_decrement(country_code: int):
    return capacity_collection.update_one(
        {"country_code": country_code},
        {"$inc": {"capacity": -1}}
    )


# ------------------ 2FA functions ------------------
def get_current_2fa():
    return admin2fa_collection.find_one()


def set_2fa_password(password: int):
    return admin2fa_collection.update_one({}, {"$set": {"2fa": password}}, upsert=True)


def update_2fa_password(new_password: int):
    return admin2fa_collection.update_one({}, {"$set": {"2fa": new_password}})


# ------------------ Support/Channel Settings ------------------
def get_settings():
    settings = settings_collection.find_one({})
    if not settings:
        default_settings = {
            "support_username": "JB_RECEIVER_SUPORT",
            "channel_username": "JB_TEAMRECHIVERBOTUPTED"
        }
        settings_collection.insert_one(default_settings)
        return default_settings
    return settings


def set_support_username(new_username: str):
    return settings_collection.update_one({}, {"$set": {"support_username": new_username}}, upsert=True)


def set_channel_username(new_username: str):
    return settings_collection.update_one({}, {"$set": {"channel_username": new_username}}, upsert=True)
