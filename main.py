import discord
import os
import random
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

@bot.command()
async def roll4life(ctx):
    # Russian roulette simulation: 1 in 6 chance to "die"
    bullet_chamber = random.randint(1, 6)

    if bullet_chamber == 1:
        # The author "dies"
        try:
            timeout_duration = timedelta(minutes=1)
            await ctx.author.timeout(timeout_duration, reason="Lost at Russian roulette")
            await ctx.send(f'{ctx.author.mention} pulled the trigger... 💥 **BANG!** You\'ve been shot! Enjoy death.')
        except discord.Forbidden:
            await ctx.send("I can't seem to be able to kill you.")
        except discord.HTTPException:
            await ctx.send("Failed to timeout you.")
    else:
        # The author survives
        await ctx.send(f'{ctx.author.mention} pulled the trigger... *click* You\'re lucky! No bullet this time.')
bot.run(BOT_TOKEN)