import discord
import googleapiclient.discovery
from discord.ext import commands, tasks
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime
import asyncio

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


class Schedule(commands.Cog):

    service: googleapiclient.discovery.Resource
    guild: None
    has_pinged: bool = False

    def __init__(self, bot):
        self.bot = bot
        self.service = None

    def cog_unload(self):
        self.update.cancel()

    @commands.command(name='link-calendar')
    @commands.has_role('Teacher')
    async def link_caldendar(self, ctx):
        creds = None
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        self.service = build('calendar', 'v3', credentials=creds)
        self.guild = ctx.guild
        self.update.start()
        await ctx.send('Calendar has been linked!')

    @commands.command(name='schedule')
    @commands.has_role('Teacher')
    async def show_schedule(self, ctx, arg):
        if self.service is None:
            await ctx.send("No calendar has been linked yet")
            return

        num_events = int(arg)
        now = datetime.datetime.now().isoformat() + '-04:00'
        events_result = self.service.events().list(calendarId='primary', timeMin=now,
                                                   maxResults=num_events, singleEvents=True,
                                                   orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            await ctx.send("No upcoming events found!")
        else:
            for event in events:
                event_name = '**' + event['summary'] + '**'
                await ctx.send(event_name)

                start = event['start'].get('dateTime', event['start'].get('date'))[:-6]
                start_datetime = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")

                end = event['end'].get('dateTime', event['end'].get('date'))[:-6]
                end_datetime = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")

                event_time = str(start_datetime.month) + '/' + str(start_datetime.day) + ', ' + \
                             str(start_datetime.hour) + ':' + str(start_datetime.minute) + '-' + \
                             str(end_datetime.hour) + ':' + str(end_datetime.minute)

                await ctx.send(event_time)

    @tasks.loop(seconds=20.0)
    async def update(self):
        self.has_pinged = False
        now = datetime.datetime.now()
        now_str = now.isoformat() + '-04:00'
        next_events = self.service.events().list(calendarId='primary', timeMin=now_str,
                                                   maxResults=3, singleEvents=True,
                                                   orderBy='startTime').execute()

        events = next_events.get('items', [])

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            start = start[:-6]
            start_datetime = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")

            if now.date() == start_datetime.date() and now.hour == start_datetime.hour and start_datetime.minute - now.minute == 10:
                channel = discord.utils.get(self.guild.channels, name='announcemints')

                for role in self.guild.roles:
                    if role.name == 'Student':
                        student = role
                        break

                event_name = '**' + event['summary'] + '**'
                await channel.send(f'{student.mention}' + ' ' + event_name + " will start in 10 minutes!")
                self.has_pinged = True

        if self.has_pinged:
            await asyncio.sleep(60)