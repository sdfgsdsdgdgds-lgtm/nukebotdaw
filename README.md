# Discord Bot på Render

En enkel Discord-bot byggd med `discord.py` och hostad på Render.

## Kommandon
- `/ping` – Testar att boten fungerar.
- `/nuke` – Visuell demo, ingen riktig data samlas.

## Deployment
1. Skapa en ny app på [Render.com](https://render.com)
2. Länka ditt GitHub-repo med dessa filer.
3. Lägg till miljövariabler i Render Dashboard:
   - `BOT_TOKEN`
   - `CLIENT_ID`
   - `GUILD_ID`
4. Deploya 🎉