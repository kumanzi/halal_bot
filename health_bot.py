import discord
import os
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_voice_state_update(member, before, after):
        if not before.channel and after.channel and member.id == 283363939163701249:
            channel = client.get_channel(1142138293581004901)
            await channel.send('KUMANZI IS HERE')

intents = discord.Intents.default()
intents.members = True

client.run(os.getenv('TOKEN'))