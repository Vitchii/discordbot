import discord

class Fach:
    syn = []
    links = []

    def __init__(self):
        return

    def createLinks(self): 
        return

    def getSynonyms(self):
        self.syn = []
        file = open("faecher/" +  self.__class__.__name__.lower() + ".txt", "r")
        self.syn = []
        for line in file:
            self.syn.append(line.strip().lower())
        file.close()
        return self.syn

    def getLinks(self):
        self.links = []
        self.createLinks()
        return self.links

    def getText(self):
        return "Noch kein Text vorhanden :/"

    def readSyns(self):
        return

    def getName(self):
        return "n/a"