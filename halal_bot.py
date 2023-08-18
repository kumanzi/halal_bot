import discord
import os
from dotenv import load_dotenv

load_dotenv()



intents = discord.Intents.default()
intents.members = True

client = MyClient(intents=intents)
client.run(os.getenv('TOKEN'))
