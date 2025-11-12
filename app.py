import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
import traceback
from threading import Thread
from flask import Flask

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
GUILD_ID = os.getenv("GUILD_ID")  # valfritt, men rekommenderat för snabb sync

# Flask liten webserver (endast om PORT är satt, för Render web service)
def run_webserver():
    app = Flask(__name__)

    @app.route("/")
    def home():
        return "Bot är igång och mår bra! 🚀"

    port = int(os.environ.get("PORT", 0))
    if port:
        print(f"Startar webserver på port {port} (Render Web Service-läge)")
        # Obs: Flask dev-server används enbart som heartbeat för Render gratisplan
        app.run(host="0.0.0.0", port=port)
    else:
        print("Ingen PORT satt — kör som Background Worker (ingen webserver startad).")

if os.environ.get("PORT"):
    Thread(target=run_webserver).start()

# ---- Discord bot setup ----
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Inloggad som {bot.user} (id: {bot.user.id})")

    # Försök sync i flera steg och logga bra info
    try:
        if GUILD_ID:
            try:
                guild_obj = discord.Object(id=int(GUILD_ID))
                synced = await bot.tree.sync(guild=guild_obj)
                print(f"✅ Slashkommandon synkade till guild {GUILD_ID}: {[c.name for c in synced]}")
                return
            except Exception as e_guild:
                print("⚠️ Misslyckades synka till specificerad guild (försöker global sync).")
                traceback.print_exc()
                # fortsätt för att försöka global sync
        # Global sync (kan ta upp till ~1 timme att synas i alla guilds)
        try:
            synced_global = await bot.tree.sync()
            print(f"✅ Global sync klar. Registrerade/uppdaterade kommandon: {[c.name for c in synced_global]}")
        except Exception as e_global:
            print("❌ Misslyckades med global slash-command sync.")
            traceback.print_exc()

    except Exception as e:
        print("❌ Okänt fel vid on_ready sync:")
        traceback.print_exc()

# ---- /nuke kommando ----
@bot.tree.command(name="nuke", description="Visar en cool nuke-effekt (fejk, samlar INTE IP)")
async def nuke(interaction: discord.Interaction):
    await interaction.response.defer()

    def progress_bar(pct: int) -> str:
        total = 20
        filled = int((pct / 100) * total)
        return "▰" * filled + "▱" * (total - filled) + f" {pct}%"

    steps = [
        ("Initiering", 0xFF9900, 10),
        ("Skannar portar", 0xFF6600, 30),
        ("Bryter igenom brandvägg", 0xFF3300, 55),
        ("Extraherar data", 0xFF0000, 80),
        ("Slutför", 0x00FF00, 100)
    ]

    embed = discord.Embed(
        title="🔴 NUKE INITIERAD",
        description="Förbereder...",
        color=0xFF9900
    )
    embed.set_footer(text="Detta är en visuell effekt — ingen data samlas.")
    msg = await interaction.followup.send(embed=embed)

    for desc, color, pct in steps:
        await asyncio.sleep(1.0)
        e = discord.Embed(
            title="🔴 NUKE",
            description=f"**{desc}**\n\n{progress_bar(pct)}",
            color=color
        )
        e.set_footer(text="Endast en demo. Inga IPs samlas eller loggas.")
        await msg.edit(embed=e)

    await asyncio.sleep(1.0)
    fake_ip = "127.0.0.1"
    final = discord.Embed(
        title="✅ KLAR",
        description=f"Operation slutförd.\n\nVisad (påhittad) IP: `{fake_ip}`\n\nDetta var en visuell demonstration — inga IPs togs eller loggades.",
        color=0x00FF00
    )
    await msg.edit(embed=final)

# ---- Starta bot ----
if not TOKEN:
    raise RuntimeError("BOT_TOKEN saknas i miljövariabler!")

# Kör bot (blockerar)
bot.run(TOKEN)
