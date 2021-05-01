
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

prefix = '!'

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command()
async def ping(ctx):
    await ctx.send('pong!')


@bot.command()
async def setuproles(ctx):
    await ctx.send('Setting up roles...')
    await ctx.guild.create_role(name="Student", colour=discord.Colour(0xFFA500))
    await ctx.guild.create_role(name="Teacher", colour=discord.Colour(0x3232FF), permissions=discord.Permissions(permissions=8))
    await ctx.guild.create_role(name="Assistant", colour=discord.Colour(0x800080))


@bot.command()
async def members(ctx):
    for member in ctx.guild.members:
        await ctx.send(member)


@bot.command()
async def setup(ctx):
    await ctx.send('Setting up class server')
    await create_category('❗-Important')
    await ctx.guild.create_text_channel('announcemints')

bot.run(TOKEN)
