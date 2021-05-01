import discord
from discord.ext import commands
import math


class Breakout(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='create-breakout')
    @commands.has_role('Teacher')
    async def create_breakout(self, ctx, arg):
        """Create breakout rooms. arg is the number of students to be placed in each breakout room.
        The caller of the command must have the role Teacher and must be connected to a voice channel.
        """
        member_per_room = int(arg)

        guild = ctx.guild

        for role in guild.roles:
            if role.name == 'Student':
                student = role
                break

        category = await guild.create_category('Breakout Rooms')

        if ctx.author.voice and ctx.author.voice.channel:
            channel = ctx.author.voice.channel
        else:
            await ctx.send("You are not connected to a voice channel")
            return

        students = []

        for member in channel.members:
            for role in member.roles:
                if role.name == 'Student':
                    students.append(member)

        num_breakout = math.ceil(len(students) / member_per_room)
        rooms = []

        for i in range(0, num_breakout):
            breakout_room = await guild.create_voice_channel('Breakout Room ' + str(i + 1), category=category)
            await breakout_room.set_permissions(student, connect=False, speak=True)
            rooms.append(breakout_room)

        for i in range(len((students))):
            await students[i].move_to(rooms[i // member_per_room])

        await ctx.send("Breakout Rooms Created!")

    @commands.command(name='end-breakout')
    @commands.has_role('Teacher')
    async def end_breakout(self, ctx):
        """Close all currently open breakout rooms and bring students to the voice channel the caller of
        the command is in. The caller of the command must have the role Teacher and must be in a voice channel.
        """
        guild = ctx.guild

        if ctx.author.voice and ctx.author.voice.channel:
            main_channel = ctx.author.voice.channel
        else:
            await ctx.send("You are not connected to a voice channel")
            return

        category_names = {category.name: category for category in guild.categories}
        if 'Breakout Rooms' not in category_names:
            await ctx.send("There are no active breakout rooms")
            return

        category = category_names['Breakout Rooms']
        members = []
        channels = []

        for channel in category.channels:
            channels.append(channel)
            for member in channel.members:
                members.append(member)

        for member in members:
            await member.move_to(main_channel)

        for channel in channels:
            await channel.delete()

        await category.delete()
        await ctx.send("Breakout Rooms Ended!")
        return

    @commands.command(name='poll')
    @commands.has_role('Teacher')
    async def create_poll(self, ctx, question, *options: str):
        """Create a poll in the text channel polls. question is the question to be asked and must be enclosed
        with quotation marks. (Ex. "What is the answer to Question 3?"). options are choice to be made available
        for the poll. There can be up to 10 options, and if there are only 2 options and each option is yes and no,
        the poll will be a yes or no poll. The command !setup must be ran before this command is evoked.
        """

        guild = ctx.guild

        poll_channel = discord.utils.get(guild.channels, name='polls')

        if poll_channel is None:
            await ctx.send('The server is not setup. Please use the command !setup')
            return

        if len(options) <= 1:
            await ctx.send('You need more than one option to make a poll!')
            return
        if len(options) > 10:
            await ctx.send('You cannot make a poll for more than 10 things!')
            return

        if len(options) == 2 and options[0] == 'yes' and options[1] == 'no':
            reactions = ['✅', '❌']
        else:
            reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

        description = []
        for x, option in enumerate(options):
            description += '\n {} {}'.format(reactions[x], option)
        embed = discord.Embed(title=question, description=''.join(description))
        react_message = await poll_channel.send(embed=embed)
        for reaction in reactions[:len(options)]:
            await react_message.add_reaction(reaction)
        embed.set_footer(text='Poll ID: {}'.format(react_message.id))




