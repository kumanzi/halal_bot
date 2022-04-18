#from https://github.com/Rapptz/discord.py/tree/v1.7.3/examples
import discord

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
#    fullmessage = message.content
#    salam = 'salam'
#    salaam = 'salaam'

    if 'salam' in message.content:
        await message.channel.send('Salam!')
    if 'salaam' in message.content:
    	await message.channel.send('Salaam!')

client.run('OTY1NDgwMjA3NDE2OTc1NDIx.Ylzzgw.FDF22hoeyCpvC8w4TC4wBsgJhCE')

