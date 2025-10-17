import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

homework_done = {}

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def done(ctx):
    user = ctx.author
    homework_done[user.id] = True
    await ctx.send(f"📚 {user.mention} marked their homework as 
**done!**")

@bot.command()
async def check(ctx, member: discord.Member = None):
    member = member or ctx.author
    if homework_done.get(member.id):
        await ctx.send(f"✅ {member.display_name} has finished their 
homework!")
    else:
        await ctx.send(f"❌ {member.display_name} hasn’t done their 
homework yet!")

@bot.command()
@commands.has_permissions(administrator=True)
async def reset(ctx):
    homework_done.clear()
    await ctx.send("🔄 Homework records have been reset by an admin.")

@bot.command()
async def helpme(ctx):
    help_text = (
        "**Homework Bot Commands**\n"
        "`!done` - Mark your homework as done\n"
        "`!check` - Check your own or someone’s status\n"
        "`!check @user` - Check another person\n"
        "`!reset` - (Admin only) Reset all records\n"
        "`!helpme` - Show this message"
    )
    await ctx.send(help_text)

bot.run(os.getenv("DISCORD_TOKEN"))

