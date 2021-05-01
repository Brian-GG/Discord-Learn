
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from breakout import Breakout

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

prefix = '!'

bot = commands.Bot(command_prefix='!', intents=intents)

bot.add_cog(Breakout(bot))


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
    ImportantCatagory = await ctx.guild.create_category('Important')
    DiscussionCatagory = await ctx.guild.create_category('Discussion')
    InClassCatagory = await ctx.guild.create_category('In-class')
    await ctx.send('Setting up class server')

    await ImportantCatagory.create_text_channel('Announcemints')
    await ImportantCatagory.create_text_channel('Work submission')
    await DiscussionCatagory.create_text_channel('General discussion')
    await DiscussionCatagory.create_text_channel('Off topic discussion')
    await DiscussionCatagory.create_voice_channel('General voice chat')
    await InClassCatagory.create_text_channel('Questions')
    await InClassCatagory.create_text_channel('No-microphone')
    await InClassCatagory.create_text_channel('Polls')

    class_room = await ctx.guild.create_voice_channel('Class', category=InClassCatagory)
    for role in ctx.guild.roles:
        if role.name == 'Student':
            student = role
            break
    await class_room.set_permissions(student, connect=True, speak=False)


@bot.command()
async def self_destruction(ctx):
    for category in ctx.guild.categories:
        await category.delete()
    for channel in ctx.guild.channels:
        await channel.delete()

bot.run(TOKEN)
