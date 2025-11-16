import os
import json
import asyncio
from dotenv import load_dotenv
from pymongo import MongoClient

# -------------------------------------------------------------------------
# MongoDB Setup
# -------------------------------------------------------------------------

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["PPEBotDB"]
collection = db["PPEPlayerData"]

# Locks (still needed for async safety)
_locks = {}

def get_lock(guild_id: int):
    if guild_id not in _locks:
        _locks[guild_id] = asyncio.Lock()
    return _locks[guild_id]


# -------------------------------------------------------------------------
# MongoDB helpers
# -------------------------------------------------------------------------

async def load_player_records(guild_id: int):
    """Load the 'records' JSON object for a guild from MongoDB."""
    async with get_lock(guild_id):
        doc = collection.find_one({"guild_id": guild_id})
        if not doc:
            return {}

        # Return the stored records dict
        return doc.get("records", {})


async def save_player_records(guild_id: int, records: dict):
    """Save (upsert) the 'records' JSON object for this guild."""
    async with get_lock(guild_id):
        collection.update_one(
            {"guild_id": guild_id},
            {"$set": {"records": records}},
            upsert=True
        )


# -------------------------------------------------------------------------
# Player utilities (unchanged)
# -------------------------------------------------------------------------

def ensure_player_exists(records: dict, player_name: str):
    """Ensure a player entry exists with at least one PPE."""
    key = player_name.lower()
    if key not in records:
        records[key] = {"ppes": [], "active_ppe": None}
    return key


def get_active_ppe(player_data: dict):
    """Return the active PPE dict, or None."""
    active_id = player_data.get("active_ppe")
    for ppe in player_data.get("ppes", []):
        if ppe["id"] == active_id:
            return ppe
    return None
