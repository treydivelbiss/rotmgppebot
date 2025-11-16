import discord
from discord.ext import commands
from discord import app_commands

def require_ppe_roles(admin_required: bool = False, player_required: bool = False):
    """Decorator to ensure PPE roles exist, and optionally require admin role."""
    async def predicate(interaction: discord.Interaction) -> bool:
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message("❌ This command can only be used inside a server.")
            return False
        # Detect if the help command or introspection is running
        if (
            interaction.command is None
            or interaction.command.qualified_name == "help"
            or interaction.invoked_with == "help"
            or isinstance(interaction.command, commands.HelpCommand)
        ):
            # ✅ Skip all checks silently
            return True

        admin_role = discord.utils.get(guild.roles, name="PPE Admin")
        player_role = discord.utils.get(guild.roles, name="PPE Player")

        # Roles missing entirely
        if not admin_role or not player_role:
            await interaction.response.send_message(
                "⚠️ Required roles are missing!\n"
                "Please ensure **PPE Admin** and **PPE Player** exist before using this command.\n"
                "You can fix this by re-inviting the bot with `Manage Roles` permission, "
                "or by manually creating the roles with !setuproles."
            )
            return False

        # If admin_required=True, make sure the user has the admin role
        if admin_required and admin_role not in interaction.user.roles:
            await interaction.response.send_message("🚫 You need the **PPE Admin** role to use this command.")
            return False
        # If player_required=True, make sure the user has the player role
        if player_required and player_role not in interaction.user.roles:
            await interaction.response.send_message("🚫 You need the **PPE Player** role to use this command.")
            return False

        # All good — continue
        return True

    return commands.check(predicate)
