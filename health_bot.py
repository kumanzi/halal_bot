import discord
import os
import time
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()
client.start_time = 0

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_voice_state_update(member, before, after):
        #Sends message if user with given id JOINS voice
        if not before.channel and after.channel and member.id == 283363939163701249:
            channel = client.get_channel(1142138293581004901)
            await channel.send('kumanzi is here')
            client.start_time = time.time()
        #Sends message if user with given id LEAVES voice
        if before.channel and not after.channel and member.id == 283363939163701249:
            channel = client.get_channel(1142138293581004901)
            end_time = time.time()
            elapsed_time = end_time - client.start_time
            await channel.send(f'kumanzi is gone (in voice for {elapsed_time:.2f} seconds)')

intents = discord.Intents.default()
intents.members = True

client.run(os.getenv('TOKEN'))