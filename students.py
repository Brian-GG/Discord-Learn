import random
import discord
from discord.ext import commands

class Work(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @commands.command(name='attendance')
    @commands.has_role('Teacher')
    async def take_attendance(self, ctx):
        """Takes the attendance of people in the Class voice channel. The caller of the command must have
        the role of Teacher"""
        #Class
        guild = ctx.guild
        members = guild.members
        self.student_list = StudentList()
        if ctx.author.voice and ctx.author.voice.channel:
            channel = ctx.author.voice.channel
        else:
            await ctx.send("You are not connected to a voice channel")
            return
        for member in members:
            if member.name == 'Discord Learn':
                continue
            else: self.student_list.addStudent(member)
        notHere = self.student_list.checkAttendence(channel.members)
        message = ''
        for i in range(len(notHere)):
            message+= notHere[i].name
            if i == len(notHere)-2:
                message+= ' and '
            elif i != len(notHere)-1:  message += ', '
        await ctx.send(message + ' are not present')

    @commands.command(name = 'Report')
    async def report(self, ctx, *args):
    """Allows a Student to report another person, and send a PM directly to the Teacher"""
        reason = ''
        nameORep = args[0]
        for i in range(1, len(args)):
            reason+= str(args[i]) + ' '
        guild = ctx.guild
        Teacher = None
        for member in guild.members:
            for role in member.roles:
                if role.name == 'Teacher':
                    Teacher = member
                    break
        await Teacher.send(ctx.message.author.name + ' reported ' + nameORep + ' for ' + reason)           
    
    @commands.command(name = 'Give')
    async def Teacher(self, ctx, arg):
    """Gives certain members in the channel the Teacher Role"""
        guild = ctx.guild
        member = ctx.message.author
        for roles in guild.roles:
            if roles.name == 'Teacher':
                role = roles
        for member in guild.members:
            if member.name == 'Vala.Ar' or member.name == 'cheesecake':
                await member.add_roles(role)

def setup(client):
    client.add_cog(Example(client))

class Classroom:
    def __init__(self, studentList, subject, ):
        self.studentList = studentList

class Event:
    def __init__(self, dueDate, startDate, typeEvent):
        self.dueDate = dueDate
        self.startDate = startDate
        self.typEvent = typeEvent

class Test(Event):
    def __init__(self, dueDate, startDate, typeEvent, duration):
        Event.__init__(self, dueDate, startDate, typeEvent)
        self.duration = duration


class StudentList:
    def __init__(self):
        self.holder = ()

    def addStudent(self, name):
        self.holder += (name,)

    def checkAttendence(self, names):  # names is a list of the users in the channel
        absents = []
        for student in self.holder:
            found = False
            for name in names:
                if name == student:
                    found = True
                    break
            if not found:
                absents.append(student)
        return absents

    def makeGroup(self, numOfGroups):
        if numOfGroups > len(self.holder):
            return ('cannot make groups of', numOfGroups)
        remainder = len(self.holder) % numOfGroups
        numOfPeoplePerGrp = len(self.holder)//numOfGroups
        groups = []
        l = list(self.holder)
        random.shuffle(l)
        rearranged = tuple(l)
        j = 0
        c = 0
        groups.append(())
        for name in rearranged:
            groups[c] += (name,)
            j+=1
            if (j == numOfPeoplePerGrp):
                groups.append(())
                j = 0
                c +=1
        return groups


# # attendence tester
# student = StudentList()
# students = ['john', 'barbara', 'jeffrey', 'jpnanda', 'panda']
# # names = ['john', 'barbara', 'jeffrey', 'jpnanda']
# for s in students:
#     student.addStudent(s)

# # print(student.checkAttendence(names))
# print(student.makeGroup(2))
