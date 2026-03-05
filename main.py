import os, sys, time, asyncio, datetime
from keep_alive import keep_alive
import discord
from discord.ext import commands
from colorama import Fore, Style

# Start the web server
keep_alive()

# Configuration (Change prefix here if you want)
PREFIX = "." 

# Load Token from Secrets
token = os.environ.get('TOKEN')

bot = commands.Bot(command_prefix=PREFIX, self_bot=True, help_command=None)

# --- ADVANCED POWER: SNIPER & AFK DATA ---
last_deleted = {}
afk_data = {"is_afk": False, "reason": ""}

@bot.event
async def on_ready():
    os.system('clear')
    print(f"{Fore.MAGENTA}SAMAEL-V2 ULTRA LOADED{Style.RESET_ALL}")
    print(f"Logged in as: {bot.user.name}")
    print(f"Prefix: {PREFIX}")

@bot.event
async def on_message(message):
    if message.author != bot.user:
        # AFK Check
        if afk_data["is_afk"] and bot.user.mentioned_in(message):
            await message.channel.send(f"🌙 **Samael AFK:** {afk_data['reason']}", delete_after=10)
        return

    # Ghost Mode: Auto-delete your commands after 5 seconds
    if message.content.startswith(PREFIX):
        await bot.process_commands(message)
        await asyncio.sleep(5)
        try: await message.delete()
        except: pass

@bot.event
async def on_message_delete(message):
    if message.author.bot: return
    last_deleted[message.channel.id] = {
        "content": message.content,
        "author": message.author.name,
        "time": datetime.datetime.now().strftime("%H:%M:%S")
    }

# --- COMMANDS ---
@bot.command()
async def snipe(ctx):
    data = last_deleted.get(ctx.channel.id)
    if data:
        await ctx.message.edit(content=f"🎯 **Snipped:** `{data['author']}`: {data['content']}")
    else:
        await ctx.message.edit(content="❌ Nothing to snipe.")

@bot.command()
async def afk(ctx, *, reason="Busy."):
    global afk_data
    afk_data = {"is_afk": True, "reason": reason}
    await ctx.message.edit(content=f"✅ AFK Enabled: {reason}")

@bot.command()
async def back(ctx):
    global afk_data
    afk_data["is_afk"] = False
    await ctx.message.edit(content="✅ Welcome back.")

@bot.command()
async def ping(ctx):
    await ctx.message.edit(content=f"🏓 Pong! `{round(bot.latency * 1000)}ms`")

if token:
    bot.run(token, log_handler=None)
else:
    print("ERROR: Add your token to Replit Secrets first!")
