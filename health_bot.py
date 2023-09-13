from typing import Optional
import discord
from discord import app_commands
import os
import time
from threading import Timer
from dotenv import load_dotenv

MY_GUILD = discord.Object(id=964434050062364684)

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

load_dotenv()
intents = discord.Intents.default()
intents.members = True
client = MyClient(intents=intents)
client.channelId = 1142138293581004901  #channel to send messages
client.userDict = {}    #dictionary of users w/ time they entered voice to keep track of time each user is in voice
client.activeUsers = 0  #number of users currently in voice
client.interval = 10  #time interval (in sec) for reminders
client.voiceTimer = Timer(.1, time.sleep(.1))
client.matthewTimer = Timer(.1, time.sleep(.1))
client.matthew = False

#checks how long users have been in voice and acts accordingly
def checkUserTimes():
    if(client.activeUsers > 0):
        for user in client.userDict:
            print(f"{user} has been in vc for {time.time() - client.userDict[user]}")
            channel = client.get_channel(client.channelId)              #get channel to send message
            client.loop.create_task(channel.send(f'<@{user}> time to get up you fat!!!'))
        client.voiceTimer.run()

client.voiceTimer = Timer(client.interval, checkUserTimes)

@client.tree.command()
@app_commands.describe(new_interval='The new reminder interval (in minutes) you want to set',)
async def interval(interaction: discord.Interaction, new_interval: Optional[float] = None):
    """Views or sets new reminder interval."""
    if(new_interval == None):
        await interaction.response.send_message(f'Current interval is {client.interval/60:.2f} min')
    else:
        client.interval = new_interval * 60
        await interaction.response.send_message(f'New interval is {client.interval/60:.2f} min (will update after all users leave voice)')

@client.tree.command()
async def matthew(interaction: discord.Interaction):
    """Toggles Matthew function."""
    client.matthew = not client.matthew
    if(client.matthew):
        await interaction.response.send_message(f'Matthew mode enabled')
    else:
        await interaction.response.send_message(f'Matthew mode disabled')

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_voice_state_update(member, before, after):
        #Sends message with user name if user JOINS voice
        if not before.channel and after.channel:
            client.userDict[member.id] = time.time()                    #save time user joined voice
            if(client.activeUsers == 0):                                #start/run timer if first user joined
                client.voiceTimer = Timer(client.interval, checkUserTimes)
                try:
                    client.voiceTimer.start()
                except:
                    client.voiceTimer.run()
            #channel = client.get_channel(client.channelId)              #get channel to send message
            #name = str(await client.fetch_user(member.id)).split('#')   #get username
            #await channel.send(f'{name[0]} joined')                     #send message indicating who joined
            client.activeUsers += 1                                     
            print(f"{client.activeUsers} users in vc")                  #update number of active users
        #Sends message with user name if a user LEAVES voice including time specific user spent in voice
        if before.channel and not after.channel:
            try:
                elapsed_time = time.time() - client.userDict[member.id] #calculate elapsed time in voice
            except:
                elapsed_time = -1
            client.userDict[member.id] = -1                             #reset dict time to show user left voice
            #channel = client.get_channel(client.channelId)              #get channel to send message
            #name = str(await client.fetch_user(member.id)).split('#')   #get username
            #await channel.send(f'{name[0]} left ({elapsed_time:.2f}s)') #send message with username and time spent in voice
            if(client.activeUsers > 0):
                client.activeUsers -= 1
            if(client.activeUsers == 0):
                client.voiceTimer.cancel()
            print(f"{client.activeUsers} users in vc")                  #update numer of active users



client.run(os.getenv('TOKEN'))