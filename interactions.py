import asyncio

import discord
from discord.ext import commands


class Interactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='raise-hand')
    @commands.has_role('Student')
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def raise_hand(self, ctx):
        student = ctx.author
        channel = discord.utils.get(ctx.guild.channels, name='questions')

        if channel is None:
            await ctx.send('The channel has not been setup yet')
            return

        await channel.send(str(student.name) + ' has requested to speak.')
        msg = await channel.send('React to the message with check to unmute ' + str(student.name) + ' or react with cross to deny request')
        reactions = ['✅', '❌']
        for reaction in reactions:
            await msg.add_reaction(reaction)

        def check(reaction, user):
            role_names = [role.name for role in user.roles]
            return 'Teacher' in role_names and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '❌')

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=120.0, check=check)
        except asyncio.TimeoutError:
            await channel.send("Request Timed Out")
            return

        if str(reaction.emoji) == '✅':
            await student.edit(mute=False)
        else:
            await channel.send('Request to speak as been denied')
            return

        done = await channel.send('React to this message with check to mute ' + str(student.name) + ' again')
        reactions = ['✅']
        for reaction in reactions:
            await done.add_reaction(reaction)

        def done_check(reaction, user):
            role_names = [role.name for role in user.roles]
            return 'Teacher' in role_names and str(reaction.emoji) == '✅'

        reaction, user = await self.bot.wait_for('reaction_add', check=done_check)

        general_vc = discord.utils.get(ctx.guild.channels, name='General voice chat')

        if user.voice and user.voice.channel:
            channel = user.voice.channel
        else:
            await ctx.send("You are not connected to a voice channel")
            return

        await student.move_to(general_vc)
        await student.move_to(channel)
