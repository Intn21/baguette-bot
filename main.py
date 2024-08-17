import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
BOT_TOKEN=os.getenv('BOT_TOKEN')
intents = discord.Intents.default()
intents.message_content = True  # This is necessary to receive message content

# Set up the bot with a command prefix (e.g., "!")
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

# Replace 'your-token-here' with your bot's token
bot.run(BOT_TOKEN)
