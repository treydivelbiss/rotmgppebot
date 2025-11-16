import os
import json
import asyncio
from typing import Dict, Any

# Persistent data directory (Railway Volume)
DATA_DIR = "/data"
os.makedirs(DATA_DIR, exist_ok=True)

# Per-guild asyncio locks
_locks: Dict[int, asyncio.Lock] = {}


def get_lock(guild_id: int) -> asyncio.Lock:
    """Return or create a lock for this guild."""
    if guild_id not in _locks:
        _locks[guild_id] = asyncio.Lock()
    return _locks[guild_id]


def get_guild_data_path(guild_id: int) -> str:
    """Return the file path for this guild's data file."""
    return os.path.join(DATA_DIR, f"{guild_id}_loot_records.json")


# -------------------------------------------------------------------------
# Core read/write functions (safe + async-friendly)
# -------------------------------------------------------------------------

async def load_player_records(guild_id: int) -> Dict[str, Any]:
    """Load player records for a specific guild safely and non-blockingly."""
    path = get_guild_data_path(guild_id)

    if not os.path.exists(path):
        return {}

    async with get_lock(guild_id):
        try:
            return await asyncio.to_thread(_read_json_file, path)
        except Exception:
            return {}  # fallback


def _read_json_file(path: str) -> Dict[str, Any]:
    """Blocking helper for reading JSON safely."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}  # corrupted file
    except Exception:
        return {}  # I/O error fallback


async def save_player_records(guild_id: int, records: dict):
    """Save player records safely using atomic write."""
    path = get_guild_data_path(guild_id)
    temp_path = f"{path}.tmp"

    async with get_lock(guild_id):
        await asyncio.to_thread(_write_atomic_json, path, temp_path, records)


def _write_atomic_json(path: str, temp_path: str, data: dict):
    """Write JSON atomically to avoid corruption."""
    # Write to temp file first
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    # Optional: backup old file
    # if os.path.exists(path):
    #     os.replace(path, f"{path}.bak")

    # Atomically replace the real file
    os.replace(temp_path, path)


# -------------------------------------------------------------------------
# Player utilities
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
