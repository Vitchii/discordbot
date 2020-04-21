import discord
import os
from discord.ext import commands

client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print('Bot is ready')

@client.command()
async def test(c):
    await c.send(f'Test successful');

@client.event
async def on_message(m):
    if m.author.Bot:
        return
    else:
        handleMessage(m)

def handleMessage(m):
    print(m);        

client.run(os.environ['DISCORD_TOKEN'])
