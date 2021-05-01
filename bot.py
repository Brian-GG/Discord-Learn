# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

prefix = '!'


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    server = message.guild
    name = message.author.name

    if prefix + 'ping' in message.content.lower():
        await message.channel.send('pong!')
    elif prefix + 'setuproles' in message.content.lower():
        await message.channel.send('Setting up roles...')
        await server.create_role(name="Student", colour=discord.Colour(0xFFA500))
        await server.create_role(name="Teacher", colour=discord.Colour(0x3232FF), permissions=discord.Permissions(permissions=8))
        await server.create_role(name="Assistant", colour=discord.Colour(0x800080))

    if message.author.roles
    if prefix + 'setup' in message.content.lower():
        await message.channel.send('Setting up class server')
        await server.create_text_channel('announcemints')


client.run(TOKEN)
