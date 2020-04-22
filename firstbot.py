import discord
from faecher.automatenundformalesprachen import Automatenundformalesprachen 
from faecher.rechnernetze import Rechnernetze
from faecher.kleinesProjekt import KleinesProjekt
from faecher.grossesProjekt import GrossesProjekt
from faecher.xmltechnologien import XmlTechnologien
from discord.ext import commands
import os

client = commands.Bot(command_prefix='.')
cl = discord.Client()
automatenObj = Automatenundformalesprachen()
rechnernetzeObj = Rechnernetze()
kleinesProjektObj = KleinesProjekt()
grossesProjektObj = GrossesProjekt()
xmlTechnologienObj = XmlTechnologien()
faecherarray = [automatenObj, rechnernetzeObj, kleinesProjektObj, grossesProjektObj, xmlTechnologienObj]


### test 

#187

@client.event
async def on_message(m):
    if m.author.bot or (m.channel.name != "info-bot" and m.channel.name != "botkanal"):
        return
 
    if m.content.startswith('!'):
        await handleMessage(m)

    await client.process_commands(m)
    



async def handleMessage(m): 
    msg = m.content.lower()[1:]
    beantwortet = False
    for f in faecherarray:
        if f.getSynonyms().__contains__(msg):
            await m.channel.send(f'{m.author.mention}: ' + f.getText())
            for l in f.getLinks():
                await m.channel.send(embed = l)
            beantwortet = True

    if not beantwortet:
        if msg == "help" or msg == "h" or msg == "hilfe":
            await m.channel.send("Übersicht der Commands:"
                                + "\n!help            Zeigt dir eine Übersicht der Commands an"
                                + "\n!*fach*            Zeigt die Links zu den Unterlagen für *fach* an"
                                + "\n!faecher      Zeigt die eine Liste der eingetragenen Fächer an"
                                + "\n!git               Sendet dir den GitHub-Link"
                                + "\n\nWer das liest ist doof :P")
            beantwortet = True
        
        if msg == "faecher" or msg == "f":
            text = "Bis jetzt sind folgende Fächer eingetragen:"
            for i in range(len(faecherarray)):
                text = text + "\n" + str(i+1) + ". " + faecherarray[i].getName()
            await m.channel.send(text)
            beantwortet = True

        if msg == "fach":
            await m.channel.send("Sehr witzig :D:D:D:D")
            beantwortet = True

        if msg == "github" or msg == "git":
            t = 'discordbot'
            u = 'https://github.com/nilslambertz/discordbot'
            d = 'Github'
            embed = discord.Embed(title=t, url=u, description=d)
            await m.channel.send(embed = embed)
            beantwortet = True

        if msg == "hurensohn":
            await m.channel.send("selber hurensohn")
            beantwortet = True
                



@client.event
async def on_ready():
    print('Bot is ready!')

@client.command()
async def test(c):
    await c.send(f'{c.author.mention}: Test erfolgreich :-)')

#client.run(os.environ['DISCORD_TOKEN'])
client.run('NzAyMTU3MjM1MTQ0NDkxMDc4' + '.XqCEaQ.ffCEfyjITgz1FeAlkqI3BckKD2U')
