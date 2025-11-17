import discord
from discord.ext import commands
from discord import app_commands

def require_ppe_roles(admin_required: bool = False, player_required: bool = False):
    async def predicate(inter: discord.Interaction):
        guild = inter.guild
        user = inter.user

        if guild is None:
            await inter.response.send_message(
                "❌ This command can only be used in a server.",
                ephemeral=True
            )
            return False

        admin_role = discord.utils.get(guild.roles, name="PPE Admin")
        player_role = discord.utils.get(guild.roles, name="PPE Player")

        if not admin_role or not player_role:
            await inter.response.send_message(
                "⚠️ Required roles are missing!\n"
                "Please ensure **PPE Admin** and **PPE Player** exist.",
                ephemeral=True
            )
            return False

        # Admin check
        if admin_required and admin_role not in user.roles:
            # Respond only if no response already sent
            if not inter.response.is_done():
                await inter.response.send_message(
                    "🚫 You need the **PPE Admin** role to use this command.",
                    ephemeral=True
                )
            return False

        # Player check
        if player_required and player_role not in user.roles:
            if not inter.response.is_done():
                await inter.response.send_message(
                    "🚫 You need the **PPE Player** role to use this command.",
                    ephemeral=True
                )
            return False

        return True

    return app_commands.check(predicate)
