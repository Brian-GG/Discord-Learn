import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from breakout import Breakout
import asyncio
from schedule import Schedule
from students import Work

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
prefix = '!'

bot = commands.Bot(command_prefix='!', intents=intents)

bot.add_cog(Breakout(bot))
bot.add_cog(Work(bot))
bot.add_cog(Schedule(bot))

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
@commands.has_role('Teacher')
async def members(ctx):
    for member in ctx.guild.members:
        await ctx.send(member)
    

@bot.command(pass_context=True)
@commands.has_role('Teacher')
async def setup(ctx):
    ImportantCatagory = await ctx.guild.create_category('Important')
    DiscussionCatagory = await ctx.guild.create_category('Discussion')
    InClassCatagory = await ctx.guild.create_category('In-class')
    await ctx.send('Setting up class server')

    welcomec = await ImportantCatagory.create_text_channel('Welcome')
    announcementsc = await ImportantCatagory.create_text_channel('Announcements')
    workc = await ImportantCatagory.create_text_channel('Work submission')
    generalc = await DiscussionCatagory.create_text_channel('General discussion')
    offc = await DiscussionCatagory.create_text_channel('Off topic discussion')
    generalv = await DiscussionCatagory.create_voice_channel('General voice chat')
    questionsc = await InClassCatagory.create_text_channel('Questions')
    nomic = await InClassCatagory.create_text_channel('No-microphone')
    pollsc = await InClassCatagory.create_text_channel('Polls')
    class_room = await ctx.guild.create_voice_channel('Class', category=InClassCatagory)
    for role in ctx.guild.roles:
        if role.name == 'Student':
            student = role
            break

    await class_room.set_permissions(student, connect=True, speak=False)
    await class_room.set_permissions(ctx.guild.roles[0], connect=True, speak=False)

    await workc.set_permissions(ctx.guild.roles[0], read_messages=False, send_messages=False)
    await generalc.set_permissions(ctx.guild.roles[0], read_messages=False, send_messages=False)
    await offc.set_permissions(ctx.guild.roles[0], read_messages=False, send_messages=False)
    await generalv.set_permissions(ctx.guild.roles[0], connect=False, speak=False)
    await questionsc.set_permissions(ctx.guild.roles[0], read_messages=False, send_messages=False)
    await nomic.set_permissions(ctx.guild.roles[0], read_messages=False, send_messages=False)
    await pollsc.set_permissions(ctx.guild.roles[0], read_messages=False, send_messages=False)
    await class_room.set_permissions(ctx.guild.roles[0], read_messages=False, send_messages=False)
    
    
    
    await workc.set_permissions(student, read_messages=True, send_messages=True)
    await generalc.set_permissions(student, read_messages=True, send_messages=True)
    await offc.set_permissions(student, read_messages=True, send_messages=True)
    await generalv.set_permissions(student, connect=True, speak=True)
    await questionsc.set_permissions(student, read_messages=True, send_messages=True)
    await nomic.set_permissions(student, read_messages=True, send_messages=True)
    await pollsc.set_permissions(student, read_messages=True, send_messages=True)
    await class_room.set_permissions(student, read_messages=True, send_messages=True)


    await welcomec.set_permissions(student,read_messages=True, send_messages=False) 
    await welcomec.set_permissions(ctx.guild.roles[0],read_messages=True, send_messages=False) 
    await announcementsc.set_permissions(student,read_messages=True, send_messages=False)
    await announcementsc.set_permissions(ctx.guild.roles[0],read_messages=False, send_messages=False)

    Welcome_channel = discord.utils.get(ctx.guild.channels, name='welcome')
    await Welcome_channel.send("Welcome to your virtual classroom environment brought to you by Discord Learn first a couple things to keep in mind:")
    await Welcome_channel.send("- Keep chat clean and be respectful to everyone")
    await Welcome_channel.send("- You will get reminder pings for scheduled events such as class")
    await Welcome_channel.send("- During class you'll be required to move into the class voice call and muted")
    await Welcome_channel.send("- Please keep discussion topics in the correct text channel")
    message = await Welcome_channel.send("That being said, react to this message with the check if you agree to these and you will get the Student role")
    guild = ctx.guild

    poll_channel = discord.utils.get(guild.channels, name='welcome')

    if poll_channel is None:
        await ctx.send('The server is not setup. Please use the command !setup')
        return
    reactions = ['✅']
    for reaction in reactions:
        await message.add_reaction(reaction)



@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message.channel.name != 'welcome':
        return
    student = None
    for role in reaction.message.guild.roles:
        if role.name == 'Student':
            student = role
            break
    
    users = await reaction.users().flatten()
    for person in users:
        await person.add_roles(student)

#    if str(reaction.emoji) == ":HotS_Tank:":
#        await bot.add_roles(user, roleHOTS_Tank)


@bot.command()
@commands.has_role('Teacher')
async def self_destruction(ctx):
    for category in ctx.guild.categories:
        await category.delete()
    for channel in ctx.guild.channels:
        await channel.delete()



bot.run(TOKEN)
