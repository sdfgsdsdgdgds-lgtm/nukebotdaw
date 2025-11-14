import discord
from discord.ext import commands
from discord import app_commands
import os
import random
from datetime import datetime, timedelta
from collections import defaultdict
import asyncio
import aiohttp
import requests

# ===== Miljövariabler =====
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
SELF_ASSIGN_ROLE_NAME = os.getenv('SELF_ASSIGN_ROLE')
DEPLOY_HOOK_URL = os.getenv('DEPLOY_HOOK_URL')
OWNER_ID = int(os.getenv('OWNER_ID', '0'))
WELCOME_CHANNEL_NAME = "welcome"

# ===== Intents =====
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

# ===== KONFIG =====
AUTO_ROLE_NAME = "Member"
ANTI_RAID_TIME_WINDOW = 60
ANTI_RAID_THRESHOLD = 5
LOCKDOWN_DURATION = 300

# ===== Variabler =====
join_times = defaultdict(list)
locked_guilds = set()
start_time = datetime.utcnow()  # För uptime

# ===== Nuke Kommando =====
@bot.tree.command(name="nuke", description="Raderar alla kanaler och rensar servern (endast ägaren)")
@app_commands.checks.has_permissions(administrator=True)
async def nuke(interaction: discord.Interaction):
    """Raderar alla kanaler och rensar servern."""
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("❌ Du har inte behörighet att använda nuke-kommandot.", ephemeral=True)
        return

    guild = interaction.guild

    try:
        # Radera alla textkanaler
        for channel in guild.text_channels:
            try:
                await channel.delete()
                print(f"🔨 Raderade kanal {channel.name}")
            except Exception as e:
                print(f"❌ Kunde inte radera kanal {channel.name}: {e}")

        # Radera alla röstkanaler
        for channel in guild.voice_channels:
            try:
                await channel.delete()
                print(f"🔨 Raderade röstkanal {channel.name}")
            except Exception as e:
                print(f"❌ Kunde inte radera röstkanal {channel.name}: {e}")

        # Ta bort alla roller (förutom @everyone)
        for role in guild.roles:
            if role.name != "@everyone":
                try:
                    await role.delete()
                    print(f"🔨 Raderade roll {role.name}")
                except Exception as e:
                    print(f"❌ Kunde inte radera roll {role.name}: {e}")

        # Skapa om @everyone-rollen med standardbehörigheter
        everyone_role = guild.get_role(guild.id)
        if everyone_role:
            await everyone_role.edit(permissions=discord.Permissions.all())
            print("🔧 Återställde @everyone-rollen.")

        # Skapa nya kanaler
        await guild.create_text_channel("general")
        await guild.create_voice_channel("General Voice")

        await interaction.response.send_message("⚠️ Servern har blivit rensad (nuked)! Allt är nu borttaget.")

    except Exception as e:
        await interaction.response.send_message(f"❌ Ett fel inträffade vid nuke: {e}", ephemeral=True)

# ===== Starta boten =====
if __name__ == "__main__":
    if not TOKEN:
        print("❌ ERROR: DISCORD_BOT_TOKEN hittades inte i miljövariablerna!")
    else:
        print("🚀 Startar Discord bot...")
        try:
            bot.run(TOKEN)
        except Exception as e:
            print(f"❌ Boten kraschade: {e}")
            if DEPLOY_HOOK_URL:
                print("🔁 Försöker starta om via Render Deploy Hook...")
                try:
                    requests.post(DEPLOY_HOOK_URL)
                    print("✅ Deploy Hook kallad — Render startar om boten.")
                except Exception as err:
                    print(f"❌ Kunde inte kalla Render Deploy Hook: {err}")
