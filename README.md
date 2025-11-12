# Discord Nuke Bot (Demo)

Denna repo innehåller en enkel Discord-bot (Python) som visar ett visuellt `/nuke`-slash-kommando (fejkad "hacking" effekt).
Den samlar **inte** IP eller annan användardata. Koden är anpassad för enkel deploy på Render.com (web service eller background worker).

## Innehåll
- `app.py` - botkoden (slash-kommando `/nuke`)
- `requirements.txt` - Python dependencies
- `render.yaml` - Render-konfiguration för enkel deploy
- `.gitignore`
- `.env.example` - exempel på miljövariabler (INGET verkligt token här)

## Setup (Render)
1. Skapa ett nytt repo på GitHub och pusha innehållet från denna mapp.
2. Gå till https://render.com och välj "New" → "Web Service".
3. Välj ditt repo och deploy. Render använder `render.yaml`.
4. Lägg till följande Environment variables i Render dashboard:
   - `BOT_TOKEN` (din Discord bot token)
   - `CLIENT_ID` (Client ID för din Discord app)
   - `GUILD_ID` (valfritt – för snabb command sync)
5. När deploy lyckas, titta i Logs. Du bör se:
   ```
   ✅ Inloggad som <din-bot>
   ```
6. Bjud in botten till din server via OAuth2 (applications.commands & bot scopes) och testa `/nuke`.

## Kör lokalt (valfritt)
1. Skapa en `.env`-fil med följande (lägg INTE upp denna fil till GitHub):
   ```
   BOT_TOKEN=din_token
   CLIENT_ID=din_client_id
   GUILD_ID=din_guild_id
   ```
2. Installera beroenden:
   ```
   pip install -r requirements.txt
   ```
3. Kör:
   ```
   python app.py
   ```

## Säkerhet
- Dela aldrig din `BOT_TOKEN`. Använd alltid miljövariabler.
- Denna bot samlar inte IP-adresser eller annan privat data.
