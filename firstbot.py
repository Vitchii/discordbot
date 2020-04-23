from faecher.automatenundformalesprachen import Automatenundformalesprachen 
from faecher.rechnernetze import Rechnernetze
from faecher.kleinesProjekt import KleinesProjekt
from faecher.grossesProjekt import GrossesProjekt
from faecher.xmltechnologien import XmlTechnologien

from suggestions.suggestions import Suggestions

import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix='.')
bot = discord.Client()

automatenObj = Automatenundformalesprachen()
rechnernetzeObj = Rechnernetze()
kleinesProjektObj = KleinesProjekt()
grossesProjektObj = GrossesProjekt()
xmlTechnologienObj = XmlTechnologien()
faecherarray = [automatenObj, rechnernetzeObj, kleinesProjektObj, grossesProjektObj, xmlTechnologienObj]

sugg = Suggestions(faecherarray)

# 187

### test 

@client.event
async def on_message(m):
    if isinstance(m.channel, discord.DMChannel) and not m.author.bot:
        print("received private message from " + m.author.name)
        await sugg.gotReply(m)
        return


    if m.author.bot or (m.channel.name != "info-bot" and m.channel.name != "botkanal"):
        return

    if m.content.startswith('!'):
        await handleMessage(m)

    await client.process_commands(m)
    



async def handleMessage(m): 
    msg = m.content.lower()[1:]
    answered = False
    for f in faecherarray:
        if f.getSynonyms().__contains__(msg):
            await m.channel.send(f'{m.author.mention}: ' + f.getText())
            for l in f.getLinks():
                await m.channel.send(embed = l)
            answered = True

    if not answered:
        if msg == "help" or msg == "h" or msg == "hilfe":
            await m.channel.send("Übersicht der Commands:"
                                + "\n!help            Zeigt dir eine Übersicht der Commands an"
                                + "\n!*fach*            Zeigt die Links zu den Unterlagen für *fach* an"
                                + "\n!faecher      Zeigt die eine Liste der eingetragenen Fächer an"
                                + "\n!git               Sendet dir den GitHub-Link"
                                + "\n\nWer das liest ist doof :P")
            answered = True
        
        if msg == "faecher" or msg == "f":
            text = "Bis jetzt sind folgende Fächer eingetragen:"
            for i in range(len(faecherarray)):
                text = text + "\n" + str(i+1) + ". " + faecherarray[i].getName()
            await m.channel.send(text)
            answered = True

        if msg == "fach":
            await m.channel.send("Sehr witzig :D:D:D:D")
            answered = True

        if msg == "github" or msg == "git":
            t = 'discordbot'
            u = 'https://github.com/nilslambertz/discordbot'
            d = 'Github'
            embed = discord.Embed(title=t, url=u, description=d)
            await m.channel.send(embed = embed)
            answered = True

        if msg == "hurensohn":
            await m.channel.send("Du bist selbst ein Hurensohn, "+ f"{m.author.mention}")
            answered = True
            
        if msg == "hoffmann":
            await m.channel.send("https://www.youtube.com/watch?v=ffp_M7RCLTI")
            answered = True

        if msg == "doofmann":
            await m.channel.send(":O")
            answered = True
                
    if not answered:
        await m.channel.send("Diesen Command kenne ich nicht :(")
        if sugg.getDenied().__contains__(str(m.author.id)):
            print(m.author.name + " doesn't want to give suggestions")
            return
        
        if not sugg.getAccepted().__contains__(str(m.author.id)):
            print("Asking " + m.author.name + " for permission")
            await sugg.askForPermission(m)

        if sugg.getAccepted().__contains__(str(m.author.id)):
            print("Asking " + m.author.name + " for suggestions")
            await sugg.suggestNewCommand(m)
        
        return







@client.event
async def on_ready():
    print('Bot is ready!')

@client.command()
async def test(c):
    await c.send(f'{c.author.mention}: Test erfolgreich :-)')

#client.run(os.environ['DISCORD_TOKEN'])
client.run('NzAyMTU3MjM1MTQ0NDkxMDc4' + '.XqCEaQ.ffCEfyjITgz1FeAlkqI3BckKD2U')