import os
import config
import nextcord
from nextcord.ext import commands

description = """An example bot to showcase the nextcord.ext.commands extension
module.

There are a number of utility commands being showcased here."""

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="$", description=description, intents=intents)

bot.remove_command('help')

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")


@bot.command()
@commands.check(config.is_owner)
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")
    await ctx.send("Loaded extension")

# @bot.command()
# @commands.check(config.is_owner)
# async def reload(ctx, extension):
#     bot.reload_extension(f"cogs.{extension}")
#     await ctx.send("Reloaded extension")

@bot.command()
@commands.check(config.is_owner)
async def unload(ctx, extension):
    bot.unload_extensions(f"cogs.{extension}")
    await ctx.send("Unloaded extension")

for fn in os.listdir("./cogs"):
    if fn.endswith(".py"):
        bot.load_extension(f"cogs.{fn[:-3]}")


bot.run(config.BOT_TOKEN)