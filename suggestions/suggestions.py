import discord
from discord.ext import commands

class Suggestions:
    denied = []
    accepted = []
    waiting = []
    newCommand = []
    bot = discord.Client()
    client = commands.Bot(command_prefix='.')

    def __init__(self):
        global denied
        global accepted
        global waiting
        global newCommand
        denied = []
        accepted = []
        waiting = []
        newCommand = []
        self.updateDenied()
        self.updateAccepted()
        return

    def updateDenied(self):
        file = open("suggestions/denied.txt", "r")
        self.denied = []
        for line in file:
            self.denied.append(line.strip().lower())
        file.close()

    def getDenied(self):
        return self.denied

    def updateAccepted(self):
        file = open("suggestions/accepted.txt", "r")
        self.accepted = []
        for line in file:
            self.accepted.append(line.strip().lower())
        file.close()
    
    def getAccepted(self):
        return self.accepted

    async def askForPermission(self, m):
        await m.author.send("Du kannst mich verbessern, indem du mir Vorschläge zur Einordnung von Commands gibst! "
                            + "Du erhältst jedes mal eine private Nachricht, wenn ich einen von dir eingegebenen Command nicht kenne und kannst diesen bestimmten "
                            + "Kategorien zuordnen. Diese Einordnung wird dann überprüft und ggf. freigeschaltet! "
                            + "\n\nWillst du mitmachen? Schreibe einfach **YES** oder **NO**")
        print(self.waiting)
        print("1")
        self.waiting.append([str(m.author.id), m.content])
        print(self.waiting)
        print("2")
        #self.waiting.append(str(m.author.id))
        print(m.author.name + " is now in the waiting queue")

    async def gotReply(self, m):
        msg = m.content.lower()
        if self.waiting[0].__contains__(str(m.author.id)):
            if msg == 'y' or msg == 'yes' or msg == 'ye' or msg == 'j' or msg == 'ja':
                file = open("suggestions/accepted.txt", "a")
                file.write(str(m.author.id))
                file.close()
                print(self.waiting)
                print("3")
                cmd = self.waiting[self.waiting[0].index(str(m.author.id))][1]
                del self.waiting[self.waiting[0].index(str(m.author.id))]
                print(self.waiting)
                print("4")
                #self.waiting.remove(str(m.author.id))
                self.updateAccepted()
                print(m.author.name + " want to help with suggestions in the future")
                await self.suggestNewCommand(m, cmd)
            else:
                if msg == 'n' or msg == 'no' or msg == 'ne' or msg == 'nein':
                    file = open("suggestions/denied.txt", "a")
                    file.write(str(m.author.id))
                    file.close()
                    print(self.waiting)
                    print("5")
                    del self.waiting[self.waiting[0].index(str(m.author.id))]
                    print(self.waiting)
                    print("6")
                    #self.waiting.remove(str(m.author.id))
                    self.updateDenied()
                    print(m.author.name + " doesn't want to help with suggestions in the future")
                    return
                else: 
                    print(m.author.name + " didn't give a valid answer")
                    await m.channel.send("Bitte mit **YES** oder **NO** antworten!")
                    return
                
    def getWaitingUsers(self):
        return self.waiting[0]

    async def suggestNewCommand(self, m, cmd = ""):
        if cmd == "":
            cmd = m.content

        await m.author.send("Wozu würdest du **" + cmd + "** zuordnen?")
        print("test")