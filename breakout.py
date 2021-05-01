from discord.ext import commands
import math


class Breakout(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='create-breakout')
    async def create_breakout(self, ctx, arg):
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
    async def end_breakout(self, ctx):
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



