import discord
import traceback
from discord.ext import commands
from os import getenv
import os
import psycopg2

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

DATABASE_URL = os.environ.get('DATABASE_URL')
with psycopg2.connect(DATABASE_URL) as conn:
    with conn.cursor() as cur:
        cur.execute("select * from kaikei")
        results = cur.fetchall()
        member_payment_dict = {}
        for (member, payment) in results:
            member_payment_dict[member] = payment

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def add(ctx, arg):
    member = str(ctx.author.name)
    delta_payment = int(arg)
    if member not in member_payment_dict.keys():
        member_payment_dict[member] = delta_payment
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO kaikei values ('{0}', {1})".format(member,delta_payment))
    else:
        new_payment = member_payment_dict[member] + delta_payment
        member_payment_dict[member] = new_payment
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE kaikei SET payment = {1} where name = '{0}'".format(member,new_payment))
    msg = '\n'.join("{0}:{1}".format(member,payment) for (member,payment) in member_payment_dict.items())
    await ctx.send(msg)
    
@bot.command()
async def test(ctx):
    await ctx.send(ctx.author.name)
    
@bot.command()
async def reload(ctx):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("select * from kaikei")
            results = cur.fetchall()
    member_payment_dict = {}
    for (member, payment) in results:
        member_payment_dict[member] = payment
        
@bot.command()
async def show(ctx):
    msg = '\n'.join("{0}:{1}".format(member,payment) for (member,payment) in member_payment_dict.items())
    await ctx.send(msg)

token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)

