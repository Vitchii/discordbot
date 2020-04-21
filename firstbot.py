import discord
import os

client = discord.Client()


@client.event
async def on_ready():
    print('Bot is ready')

@client.event
async def on_message(m):
    if m.author.bot:
        return
    else:
        handleMessage(m)

def handleMessage(m):
    print(m)        
    await m.channel.send("Working")

client.run(os.environ['DISCORD_TOKEN'])
