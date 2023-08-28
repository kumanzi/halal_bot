import discord
import os
import schedule
import time
from threading import Timer
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()
client.channelId = 1142138293581004901  #channel to send messages
client.userDict = {}    #dictionary of users w/ time they entered voice to keep track of time each user is in voice
client.activeUsers = 0  #number of users currently in voice
client.interval = 10  #time interval (in sec) for reminders
client.voiceTimer = Timer(.1, time.sleep(.1))
# client.voiceTimer.start()

#checks how long users have been in voice and acts accordingly
def checkUserTimes():
    if(client.activeUsers > 0):
        for user in client.userDict:
            print(f"{user} has been in vc for {time.time() - client.userDict[user]}")
        client.voiceTimer.run()

client.voiceTimer = Timer(client.interval, checkUserTimes)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_voice_state_update(member, before, after):
        #Sends message with user name if user JOINS voice
        if not before.channel and after.channel:
            client.userDict[member.id] = time.time()                    #save time user joined voice
            if(client.activeUsers == 0):
                try:
                    client.voiceTimer.start()
                except:
                    client.voiceTimer.run()
            channel = client.get_channel(client.channelId)              #get channel to send message
            name = str(await client.fetch_user(member.id)).split('#')   #get username
            await channel.send(f'{name[0]} joined')                     #send message indicating who joined
            client.activeUsers += 1                                     
            print(f"{client.activeUsers} users in vc")                  #update number of active users
        #Sends message with user name if a user LEAVES voice including time specific user spent in voice
        if before.channel and not after.channel:
            elapsed_time = time.time() - client.userDict[member.id]     #calculate elapsed time in voice (NEED TO ADD TRY CASE)
            client.userDict[member.id] = -1                             #reset dict time to show user left voice
            channel = client.get_channel(client.channelId)              #get channel to send message
            name = str(await client.fetch_user(member.id)).split('#')   #get username
            await channel.send(f'{name[0]} left ({elapsed_time:.2f}s)') #send message with username and time spent in voice
            client.activeUsers -= 1                   
            # if(client.activeUsers == 0):
                #  client.voiceTimer.wait()
            print(f"{client.activeUsers} users in vc")                  #update numer of active users

intents = discord.Intents.default()
intents.members = True

client.run(os.getenv('TOKEN'))