import discord
import traceback
from discord.ext import commands
from os import getenv

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)
member_list = []

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def add_user(ctx, arg):
    member_list.add(arg)
    await ctx.send(' '.join(member_list))
    

@bot.command()
async def show(ctx, arg):
    await ctx.send(' '.join(member_list))

token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)

