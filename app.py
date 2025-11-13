import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
import traceback
import logging
from threading import Thread
from flask import Flask

# =====================================================
#  LOGGNING & MILJÖVARIABLER
# =====================================================
load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("bot_debug")

TOKEN = os.getenv("BOT_TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
GUILD_ID = os.getenv("GUILD_ID")
PORT = os.getenv("PORT")

logger.info("🔍 Miljövariabler:")
logger.info(f"BOT_TOKEN finns: {bool(TOKEN)}")
logger.info(f"CLIENT_ID: {CLIENT_ID}")
logger.info(f"GUILD_ID: {GUILD_ID}")
logger.info(f"PORT: {PORT}")

if not TOKEN:
    raise RuntimeError("❌ BOT_TOKEN saknas i miljövariabler!")

# =====================================================
#  WEBBSERVER (för Render / ping)
# =====================================================
def run_webserver():
    app = Flask(__name__)

    @app.route("/")
    def home():
        return "✅ Bot är igång (Render debug-läge)"

    port = int(os.environ.get("PORT", 0))
    if port:
        logger.info(f"🌐 Startar Flask-webserver på port {port}")
        app.run(host="0.0.0.0", port=port)
    else:
        logger.warning("💤 Ingen PORT satt — ingen Flask-webserver startas.")

if PORT:
    Thread(target=run_webserver, daemon=True).start()

# =====================================================
#  DISCORD-BOT SETUP
# =====================================================
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    logger.info(f"✅ Inloggad som {bot.user} (ID: {bot.user.id})")

    try:
        if GUILD_ID:
            guild = discord.Object(id=int(GUILD_ID))
            synced = await bot.tree.sync(guild=guild)
            logger.info(f"🔁 Synkade {len(synced)} kommandon till GUILD {GUILD_ID}: {[c.name for c in synced]}")
        else:
            synced = await bot.tree.sync()
            logger.info(f"🌍 Global sync: {[c.name for c in synced]}")
    except Exception:
        logger.error("❌ Fel vid slash-kommandosynk:")
        logger.error(traceback.format_exc())

@bot.event
async def on_error(event_method, *args, **kwargs):
    logger.error(f"🚨 Global Discord-fel i event '{event_method}'")
    logger.error(traceback.format_exc())

# =====================================================
#  TESTKOMMANDON
# =====================================================
@bot.tree.command(name="ping", description="Testar om boten svarar.")
async def ping(interaction: discord.Interaction):
    try:
        await interaction.response.send_message("🏓 Pong! Jag fungerar!")
        logger.info(f"/ping kördes av {interaction.user}")
    except Exception:
        logger.error("Fel i /ping:")
        logger.error(traceback.format_exc())

# =====================================================
#  STARTA BOT
# =====================================================
try:
    logger.info("🚀 Startar Discord-bot...")
    bot.run(TOKEN, log_handler=None, log_level=logging.DEBUG)
except Exception:
    logger.critical("💀 Kunde inte starta boten!")
    logger.critical(traceback.format_exc())