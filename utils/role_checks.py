import discord
from discord.ext import commands
from discord import app_commands

def require_ppe_roles(admin_required: bool = False, player_required: bool = False):
    async def predicate(inter: discord.Interaction):
        guild = inter.guild
        if guild is None:
            raise app_commands.CheckFailure(
                "❌ This command can only be used inside a server."
            )

        author = inter.user

        admin_role = discord.utils.get(guild.roles, name="PPE Admin")
        player_role = discord.utils.get(guild.roles, name="PPE Player")

        if not admin_role or not player_role:
            raise app_commands.CheckFailure(
                "⚠️ Required roles are missing!\n"
                "Please ensure **PPE Admin** and **PPE Player** exist."
            )

        if admin_required and admin_role not in author.roles:
            raise app_commands.CheckFailure(
                "🚫 You need the **PPE Admin** role to use this command."
            )

        if player_required and player_role not in author.roles:
            raise app_commands.CheckFailure(
                "🚫 You need the **PPE Player** role to use this command."
            )

        return True

    return app_commands.check(predicate)
