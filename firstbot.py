import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print('Bot is ready!')

@client.command()
async def test(c):
    await c.author.send('Test')

client.run(os.environ['DISCORD_TOKEN'])
