import discord
from discord.ext import commands

class Suggestions:
    denied = []
    accepted = []
    waiting = []
    newCommand = []
    categories = []
    suggestionInProgress = []
    bot = discord.Client()
    client = commands.Bot(command_prefix='.')

    def __init__(self, faecher):
        for f in faecher:
            self.categories.append(f.getName())
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

    async def addUserToAccepted(self, m):
        self.removeUser(str(m.author.id))
        file = open("suggestions/accepted.txt", "a")
        file.write(str(m.author.id) + "\n")
        file.close()
        self.updateAccepted()
        await m.author.send("Du kannst nun private Nachrichten erhalten!")

        return

    async def addUserToDenied(self, m):
        self.removeUser(str(m.author.id))   
        file = open("suggestions/denied.txt", "a")
        file.write(str(m.author.id) + "\n")
        file.close()
        self.updateDenied()
        await m.author.send("Du wirst nun keine privaten Nachrichten mehr erhalten!")

        return

    def removeUser(self, id):
        self.updateAccepted()
        self.updateDenied()
        if self.accepted.__contains__(id):
            with open("suggestions/accepted.txt", "r") as f:
                lines = f.readlines()
            with open("suggestions/accepted.txt", "w") as f:
                for line in lines:
                    if line.strip("\n") != id:
                        f.write(line)
 
        if self.denied.__contains__(id):
            with open("suggestions/denied.txt", "r") as f:
                lines = f.readlines()
            with open("suggestions/denied.txt", "w") as f:
                for line in lines:
                    if line.strip("\n") != id:
                        f.write(line)

        self.updateAccepted()
        self.updateDenied()
        return

    async def askForPermission(self, m):
        await m.author.send("Du kannst mich verbessern, indem du mir Vorschläge zur Einordnung von Commands gibst! "
                            + "Du erhältst jedes mal eine private Nachricht, wenn ich einen von dir eingegebenen Command nicht kenne und kannst diesem bestimmte "
                            + "Kategorien zuordnen. Diese Einordnung wird dann überprüft und ggf. freigeschaltet! "
                            + "\n\nWillst du mitmachen? Schreibe einfach **YES** oder **NO**")

        if self.waiting and self.waiting[0].__contains__(str(m.author.id)):
            return

        self.waiting.append([str(m.author.id), m.content])
        print(m.author.name + " is now in the waiting queue")

    async def gotReply(self, m):
        msg = m.content.lower()
        if self.waiting and self.waiting[0].__contains__(str(m.author.id)):
            if msg == 'y' or msg == 'yes' or msg == 'ye' or msg == 'j' or msg == 'ja':
                self.addUserToAccepted(str(m.author.id))
                cmd = self.waiting[self.waiting[0].index(str(m.author.id))][1]
                del self.waiting[self.waiting[0].index(str(m.author.id))]
                self.updateAccepted()
                print(m.author.name + " wants to help with suggestions in the future")
                await self.suggestNewCommand(m, cmd)
                return
            else:
                if msg == 'n' or msg == 'no' or msg == 'ne' or msg == 'nein':
                    self.addUserToDenied(str(m.author.id))
                    del self.waiting[self.waiting[0].index(str(m.author.id))]
                    self.updateDenied()
                    print(m.author.name + " doesn't want to help with suggestions in the future")
                    return
                else: 
                    print(m.author.name + " didn't give a valid answer")
                    await m.channel.send("Bitte mit **YES** oder **NO** antworten!")
                    return

        if self.suggestionInProgress and self.suggestionInProgress[0].__contains__(str(m.author.id)):
            await self.suggestionMade(m)
                
    def getWaitingUsers(self):
        return self.waiting[0]

    async def suggestNewCommand(self, m, cmd = ""):
        if cmd == "":
            cmd = m.content

        if self.suggestionInProgress and self.suggestionInProgress[0].__contains__(str(m.author.id)):
            del self.suggestionInProgress[self.suggestionInProgress[0].index(str(m.author.id))]
        
        self.suggestionInProgress.append([str(m.author.id), cmd])

        msg = "Wozu würdest du **" + cmd + "** zuordnen?"
        for i in range(len(self.categories)):
            msg = msg + "\n" + str(i) + ".\t" + self.categories[i]

        msg = msg + "\nGib die Zahl der Kategorie ein, die am besten zu dem Command passt!"

        await m.author.send(msg)

    async def suggestionMade(self, m):
        index = self.suggestionInProgress[0].index(str(m.author.id))

        if(m.content == "x"):
            await m.author.send("Vorgang abgebrochen!")
            del self.suggestionInProgress[self.suggestionInProgress[0].index(str(m.author.id))]
            return

        if not (m.content.isalpha() and self.categories and self.categories.__contains__(m.content)) and not (m.content.isdigit() and int(m.content) in range(len(self.categories))):
            await m.author.send("Keine valide Eingabe, bitte gib eine Zahl zwischen 0 und " + str(len(self.categories) - 1) + " ein!"
                                + "\nZum Abbrechen gib einfach \"x\" ein")
            return
            
        cat = m.content


        if cat.isdigit():
            cat = self.categories[int(cat)]


        file = open("suggestions/suggestions.txt", "a")
        file.write("{" + m.author.name + "} - {" + self.suggestionInProgress[index][1] + "} - {" + cat + "}\n")
        file.close()
        del self.suggestionInProgress[self.suggestionInProgress[0].index(str(m.author.id))]
        await m.author.send("Danke für deinen Vorschlag!")
    