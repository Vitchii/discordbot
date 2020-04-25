import discord
from faecher.fach import Fach

class XmlTechnologien(Fach):
    def __init__(self):
        self.filename = "xmltechnologien"
        pass

    def createLinks(self):
        t = 'XML-Technologien Videos'
        u = 'https://studip.uni-trier.de/dispatch.php/course/files/index/d027257c9b8850ab836e0e65e3007770?cid=f9874bc2db01bf0e4ee99fea26e4d218'
        d = 'StudIP'
        embed = discord.Embed(title=t, url=u, description=d)
        self.links.append(embed)

        t = 'XML-Technologien Folien'
        u = 'https://studip.uni-trier.de/dispatch.php/course/files/index/d9698f12543b1eb96a85fd5156ca7527?cid=f9874bc2db01bf0e4ee99fea26e4d218'
        d = 'StudIP'
        embed = discord.Embed(title=t, url=u, description=d)
        self.links.append(embed)

    def getText(self):
        return "Die Unterlagen zu __**XML-Technolgien**__ findest du hier:"

    def getName(self):
        return "XML-Technologien"

    def getShortName(self):
        return "xml"