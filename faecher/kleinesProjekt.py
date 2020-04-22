import discord
from faecher.fach import Fach

class KleinesProjekt(Fach):
    def __init__(self):
        self.filename = "kleinesProjekt"
        pass

    def createLinks(self):
        t = 'Kleines-Projekt Livestreams'
        u = 'https://moodle.uni-trier.de/course/view.php?id=77'
        d = 'Moodle'
        embed = discord.Embed(title=t, url=u, description=d)
        self.links.append(embed)

    def getText(self):
        return "Die Unterlagen zum __**kleinen Studienprojekt**__ findest du hier:"

    def getName(self):
        return "Kleines Studienprojekt"