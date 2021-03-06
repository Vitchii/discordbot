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

cmds = []
cmds.append(["!help", "Zeigt dir eine Übersicht der Commands an"])
cmds.append(["!*fach*", "Zeigt die Links zu den Unterlagen für *fach* an"])
cmds.append(["!faecher", "Zeigt die eine Liste der eingetragenen Fächer an"])
cmds.append(["!suggestions", "Erklärt dir die Suggestion-Funktion"])
cmds.append(["!accept", "Akzeptiere, dass du private Nachrichten erhältst, um den Bot zu verbessern"])
cmds.append(["!decline", "Lehne private Nachrichten durch den Bot ab"])

cmds.append(["!git", "Sendet dir den GitHub-Link"])

cmdArray = []
cmdArray.append([["hurensohn"], "Du bist selbst ein Hurensohn"])
cmdArray.append([["hoffmann"], "https://www.youtube.com/watch?v=ffp_M7RCLTI"])
cmdArray.append([["doofmann"], ":o"])
cmdArray.append([["andi"], "Ich habe eine andere Rechtsauffassung als der EuGH"])
cmdArray.append([["fach"], "Sehr witzig :D:D:D:D"])

sugg = Suggestions(faecherarray)


@client.event
async def on_message(m):
    if isinstance(m.channel, discord.DMChannel) and not m.author.bot:
        print("received private message from " + m.author.name)
        await sugg.gotReply(m)
        return

    if m.author.bot or (m.channel.name != "info-bot" and m.channel.name != "botkanal"):
        return

    if m.content.startswith('!') and m.content[1:].isalpha():
        await handleMessage(m)

    await client.process_commands(m)


async def handleMessage(m):
    msg = m.content.lower()[1:]
    answered = False
    for f in faecherarray:
        if f.getSynonyms().__contains__(msg):
            await m.channel.send(f'{m.author.mention}: ' + f.getText())
            for l in f.getLinks():
                await m.channel.send(embed=l)
            answered = True

    if not answered:
        if msg == "help" or msg == "h" or msg == "hilfe":
            text = "Übersicht der Commands:\n"
            for c in cmds:
                text = text + c[0] + "\t\t" + c[1] + "\n"

            text = text + "\n\nWer das liest ist doof :P"
            await m.channel.send(text)
            answered = True

        if msg == "faecher" or msg == "f":
            text = "Bis jetzt sind folgende Fächer eingetragen:"
            for i in range(len(faecherarray)):
                text = text + "\n" + str(i + 1) + ". " + faecherarray[i].getName() + " (" + faecherarray[
                    i].getShortName() + ")"
            await m.channel.send(text)
            answered = True

        if msg == "github" or msg == "git":
            t = 'discordbot'
            u = 'https://github.com/nilslambertz/discordbot'
            d = 'Github'
            embed = discord.Embed(title=t, url=u, description=d)
            await m.channel.send(embed=embed)
            answered = True

        for c in cmdArray:
            if msg in c[0]:
                await m.channel.send(c[1])
                answered = True

        if msg == "a" or msg == "accept":
            await sugg.addUserToAccepted(m)
            answered = True

        if msg == "d" or msg == "decline":
            await sugg.addUserToDenied(m)
            answered = True

        if msg == "suggestion" or msg == "suggestions":
            await m.channel.send(
                "Du kannst den Bot verbessern, indem du ihm Vorschläge zur Einordnung von Commands gibst! "
                + "Du erhältst jedes mal eine private Nachricht, wenn er einen von dir eingegebenen Command nicht kennt und kannst diesem bestimmte "
                + "Kategorien zuordnen. Diese Einordnung wird dann überprüft und ggf. freigeschaltet! "
                + "Du kannst mit **!accept** zustimmen und mit **!decline** ablehnen")
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

# get api key if not run on the server
try:
    file = open("apikey.txt", "r")
    key = file.readline()
except FileNotFoundError:
    print("File not found")
    key = ""

client.run(os.environ.get('DISCORD_TOKEN', key))

