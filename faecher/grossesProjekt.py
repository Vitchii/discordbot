import discord
from faecher.fach import Fach

class GrossesProjekt(Fach):
    def __init__(self):
        self.filename = "grossesProjekt"
        pass

    def createLinks(self):
        t = 'Großes-Projekt Livestreams'
        u = 'https://moodle.uni-trier.de/course/view.php?id=73'
        d = 'Moodle'
        embed = discord.Embed(title=t, url=u, description=d)
        self.links.append(embed)

    def getText(self):
        return "Die Unterlagen zum __**großen Studienprojekt**__ findest du hier:"

    def getName(self):
        return "Großes Studienprojekt (gr)"