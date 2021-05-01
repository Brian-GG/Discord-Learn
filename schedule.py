import discord
import googleapiclient.discovery
from discord.ext import commands, tasks
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


class Schedule(commands.Cog):

    service: googleapiclient.discovery.Resource

    def __init__(self, bot):
        self.bot = bot
        self.service = None

    @commands.command(name='link-calendar')
    async def link_caldendar(self, ctx):
        creds = None
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        self.service = build('calendar', 'v3', credentials=creds)
        await ctx.send('Calendar has been linked!')

    @commands.command(name='schedule')
    async def show_schedule(self, ctx, arg):
        if self.service is None:
            await ctx.send("No calendar has been linked yet")
            return

        num_events = int(arg)
        now = datetime.datetime.utcnow().isoformat() + 'Z'
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

                start = event['start'].get('dateTime', event['start'].get('date'))
                start_time = 'Start: ' + str(start.month) + '/' + str(start.day) + ', ' + \
                             str(start.hour) + ':' + str(start.minute)
                await ctx.send(start_time)


    #
    # @tasks.loop(seconds=20.0)
    # async def update(self):