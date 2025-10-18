import discord
from discord.ext import commands
import os

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="|", intents=intents)

# In-memory task store
tasks = {}

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def add(ctx, *, task: str):
    """Add a homework task."""
    user = ctx.author
    tasks[user.id] = task
    await ctx.send(f"{user.mention} added a new task: {task}")

@bot.command()
async def done(ctx):
    """Marks your homework as done."""
    user = ctx.author
    if user.id in tasks and tasks[user.id]:
        await ctx.send(f"{user.mention} marked their homework as done: {tasks[user.id]}")
        del tasks[user.id]
    else:
        await ctx.send(f"{user.mention}, you do not have any task to complete!")

@bot.command()
async def check(ctx, member: discord.Member = None):
    member = member or ctx.author
    if member.id in tasks:
        await ctx.send(f"{member.display_name} still needs to do: {tasks[member.id]}")
    else:
        await ctx.send(f"{member.display_name} has no pending tasks!")

@bot.command()
async def reset(ctx):
    if ctx.author.guild_permissions.administrator:
        tasks.clear()
        await ctx.send("All homework records have been reset by an admin.")
    else:
        await ctx.send("You do not have permission to reset homework data.")

# Run
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
