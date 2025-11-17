import discord
from discord.ext import commands
from discord import app_commands
import logging

log = logging.getLogger("ppe_checks")

def require_ppe_roles(admin_required: bool = False, player_required: bool = False):
    async def predicate(inter: discord.Interaction):
        guild = inter.guild
        user = inter.user

        if guild is None:
            log.warning(f"[IGNORED] {user} attempted to use a guild-only command in DMs.")
            return False

        admin_role = discord.utils.get(guild.roles, name="PPE Admin")
        player_role = discord.utils.get(guild.roles, name="PPE Player")

        if not admin_role or not player_role:
            log.warning(
                f"[IGNORED] {user} used command but required roles are missing "
                f"(Admin exists: {bool(admin_role)}, Player exists: {bool(player_role)})."
            )
            return False

        # Admin check
        if admin_required and admin_role not in user.roles:
            log.info(f"[DENIED] {user} attempted admin-only command without PPE Admin.")
            return False

        # Player check
        if player_required and player_role not in user.roles:
            log.info(f"[DENIED] {user} attempted player-only command without PPE Player.")
            return False

        return True

    return app_commands.check(predicate)
