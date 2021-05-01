from discord.ext import commands


class Breakout(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='create-breakout')
    async def create_breakout(self, ctx, arg):

        guild = ctx.guild

        category = await guild.create_category('Breakout Rooms')

        if ctx.author.voice and ctx.author.voice.channel:
            channel = ctx.author.voice.channel
        else:
            await ctx.send("You are not connected to a voice channel")
            return

        students = []
        

        breakout_room = await guild.create_voice_channel('Breakout Room 1', category=category)


