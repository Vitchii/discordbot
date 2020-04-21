import discord
import os
from discord.ext import commands

client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print('Bot is ready')

@client.command()
async def ping(c):
    await c.send(f'TEST');

client.run(os.environ['DISCORD_TOKEN'])
