import discord
import sys
from faecher.fach import Fach

class Automatenundformalesprachen(Fach):
    def __init__(self):
        self.filename = "automatenundformalesprachen"
        pass

    def createLinks(self):
        t = 'AFS-Livestreams'
        u = 'https://moodle.uni-trier.de/course/view.php?id=79'
        d = 'Moodle'
        embed = discord.Embed(title=t, url=u, description=d)
        self.links.append(embed)

        t = 'AFS-Vorlesungen & Audios'
        u = 'https://studip.uni-trier.de/dispatch.php/course/files/index?cid=13a0502db244f06c9479cb226a406c9c'
        d = 'StudIP'
        embed = discord.Embed(title=t, url=u, description=d)
        self.links.append(embed)

        t = 'AFS-Übungen'
        u = 'https://studip.uni-trier.de/dispatch.php/course/files/index?cid=9d02eb97e531795a5780ce84739f81b1'
        d = 'StudIP'
        embed = discord.Embed(title=t, url=u, description=d)
        self.links.append(embed)

    def getText(self):
       return "Die Unterlagen zu __**AFS**__ findest du hier:"

    def getName(self):
        return "Automaten und Formale Sprachen (afs)"

    def getShortName(self):
        return "afs"