import discord
from discord.ext import commands

client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print('Bot is ready')

@client.command()
async def random(c):
    c.send()

client.run('NzAyMTU3MjM1MTQ0NDkxMDc4.Xp8AsA.sF30YKF5V_okDh0fyDdQNyXi_JY')
