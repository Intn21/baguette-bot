import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from datetime import timedelta

load_dotenv()
BOT_TOKEN=os.getenv('BOT_TOKEN')
AUTHORIZED_USER_ID=int(os.getenv('USER_ID'))
intents = discord.Intents.default()
intents.message_content = True  # This is necessary to receive message content
intents.members = True

# Set up the bot with a command prefix (e.g., "!")
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

@bot.command()
async def timeout(ctx, member: discord.Member, duration: int, *, reason=None):
    if ctx.author.id != AUTHORIZED_USER_ID:
        await ctx.send("You are not cool enough to use this command.")
        return
    try:
        # Duration is in minutes; convert it to seconds for the timeout
        timeout_duration = timedelta(minutes=duration)

        # Timeout the member
        await member.timeout(timeout_duration, reason=reason)
        await ctx.send(f'{member.mention} has been timed out for {duration} minutes.')

    except discord.Forbidden:
        await ctx.send("I don't have permission to timeout this member.")
    except discord.HTTPException:
        await ctx.send("Failed to timeout the member.")


bot.run(BOT_TOKEN)