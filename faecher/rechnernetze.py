import discord
from faecher.fach import Fach

class Rechnernetze(Fach):
    def __init__(self):
        self.filename = "rechnernetze"
        pass

    def createLinks(self):
        t = 'Rechnernetze-Videos'
        u = 'https://studip.uni-trier.de/plugins.php/panoptoplugin/video/all?cid=a671c8313e830fd3cc792f665396da75'
        d = 'StudIP'
        embed = discord.Embed(title=t, url=u, description=d)
        self.links.append(embed)

        t = 'Rechnernetze-Folien'
        u = 'https://studip.uni-trier.de/dispatch.php/course/files/index/c5f25b0e265396c3d7fb9d9248b43206?cid=a671c8313e830fd3cc792f665396da75'
        d = 'StudIP'
        embed = discord.Embed(title=t, url=u, description=d)
        self.links.append(embed)

        t = 'Rechnerstrukturen-Videos (Backup)'
        u = 'https://www.dropbox.com/sh/hd8h2vn5219akxr/AABA1Sx5SWoVqxjq2Dj31pQwa?dl=0'
        d = 'Dropbox (Passwort: frikadelle)'
        embed = discord.Embed(title=t, url=u, description=d)
        self.links.append(embed)

    def getText(self):
        return "Die Unterlagen zu __**Rechnernetze**__ findest du hier:"

    def readSyns(self):
        return

    def getName(self):
        return "Rechnernetze"

    def getShortName(self):
        return "rn"