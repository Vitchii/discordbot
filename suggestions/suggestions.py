import discord
from discord.ext import commands


class Suggestions:
    denied = []
    accepted = []
    waiting = []
    newCommand = []
    categories = []
    suggestionInProgress = []
    reviewInProgress = []
    faecherarray = []
    admins = ["218071499943182336"]
    bot = discord.Client()
    client = commands.Bot(command_prefix='.')

    def __init__(self, faecher):
        for f in faecher:
            self.categories.append([f.getName(), f.getShortName()])
            self.faecherarray.append(f)
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
        if id in self.accepted:
            with open("suggestions/accepted.txt", "r") as f:
                lines = f.readlines()
            with open("suggestions/accepted.txt", "w") as f:
                for line in lines:
                    if line.strip("\n") != id:
                        f.write(line)

        if id in self.denied:
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

        if self.waiting and str(m.author.id) in self.waiting[0]:
            return

        self.waiting.append([str(m.author.id), m.content])
        print(m.author.name + " is now in the waiting queue")

    async def gotReply(self, m):
        msg = m.content.lower()
        if self.waiting and str(m.author.id) in self.waiting[0]:
            if msg == 'y' or msg == 'yes' or msg == 'ye' or msg == 'j' or msg == 'ja':
                await self.addUserToAccepted(m)
                cmd = self.waiting[self.waiting[0].index(str(m.author.id))][1]
                del self.waiting[self.waiting[0].index(str(m.author.id))]
                self.updateAccepted()
                print(m.author.name + " wants to help with suggestions in the future")
                await self.suggestNewCommand(m, cmd)
                return
            else:
                if msg == 'n' or msg == 'no' or msg == 'ne' or msg == 'nein':
                    await self.addUserToDenied(m)
                    del self.waiting[self.waiting[0].index(str(m.author.id))]
                    self.updateDenied()
                    print(m.author.name + " doesn't want to help with suggestions in the future")
                    return
                else:
                    print(m.author.name + " didn't give a valid answer")
                    await m.channel.send("Bitte mit **YES** oder **NO** antworten!")
                    return

        if self.suggestionInProgress and str(m.author.id) in self.suggestionInProgress[0]:
            await self.suggestionMade(m)

        if self.reviewInProgress and str(m.author.id) in self.admins:
            await self.reviewed(m)
            return

        if not self.reviewInProgress and str(m.author.id) in self.admins \
                and m.content == "!review" or m.content == "!r":
            await self.startNewReview(m)

    def getWaitingUsers(self):
        return self.waiting[0]

    async def suggestNewCommand(self, m, cmd=""):
        if cmd == "":
            cmd = m.content

        if self.suggestionInProgress and str(m.author.id) in self.suggestionInProgress[0]:
            del self.suggestionInProgress[self.suggestionInProgress[0].index(str(m.author.id))]

        self.suggestionInProgress.append([str(m.author.id), cmd])

        msg = "Wozu würdest du **" + cmd + "** zuordnen?"
        for i in range(len(self.categories)):
            msg = msg + "\n" + str(i) + ".\t" + self.categories[i][0] + " (" + self.categories[i][1] + ")"

        msg = msg + "\nGib die Zahl der Kategorie ein, die am besten zu dem Command passt! (**x** zum Abbrechen)"

        await m.author.send(msg)

    async def suggestionMade(self, m):
        index = self.suggestionInProgress[0].index(str(m.author.id))

        if (m.content.lower() == "x"):
            await m.author.send("Vorgang abgebrochen!")
            del self.suggestionInProgress[self.suggestionInProgress[0].index(str(m.author.id))]
            return

        inCategories = False
        for e in self.categories:
            if e[1] == m.content.lower():
                inCategories = True
                break

        if not (m.content.isalpha() and self.categories and inCategories) and not (
                m.content.isdigit() and int(m.content) in range(len(self.categories))):
            await m.author.send(
                "Keine valide Eingabe, bitte gib eine Zahl zwischen 0 und " + str(len(self.categories) - 1) + " ein!"
                + "\nZum Abbrechen gib einfach \"x\" ein")
            return

        cat = m.content.lower()

        if cat.isdigit():
            cat = self.categories[int(cat)][1]

        file = open("suggestions/suggestions.txt", "a")
        file.write("{" + m.author.name + "} - {" + self.suggestionInProgress[index][1] + "} - {" + cat + "}\n")
        file.close()
        del self.suggestionInProgress[self.suggestionInProgress[0].index(str(m.author.id))]
        await m.author.send("Danke für deinen Vorschlag!")

    async def startNewReview(self, m):
        file = open("suggestions/suggestions.txt", "r")
        l = file.readline()
        if l == "":
            await m.author.send("Keine ausstehenden Vorschläge zum Bewerten vorhanden!")
            return

        all = ""
        for line in file.readlines():
            all = all + line  # + "\n"
        file.close()
        file = open("suggestions/suggestions.txt", "w")
        file.write(all)
        file.close()

        user = l[1:l.index("}")]
        l = l[l.index("}") + 5:]

        cmd = l[0:l.index("}")]
        l = l[l.index("}") + 5:]

        sug = l[0:l.index("}")]

        self.reviewInProgress.append([str(m.author.id), user, cmd, sug])

        await m.author.send("Vorschlag von " + user + ":"
                            + "\n**" + cmd + "** gehört zu **" + sug + "**"
                            + "\nIst dieser Vorschlag korrekt? Bitte **YES** oder **NO** antworten!")
        return

    async def reviewed(self, m):
        answer = m.content.lower()
        index = -1
        for e in range(len(self.reviewInProgress)):
            if self.reviewInProgress[e][0] == str(m.author.id):
                index = e
                break

        if index == -1:
            await m.author.send("Es ist ein Fehler aufgetreten")
            print("User not in reviewInProgress")
            return

        if answer == "y" or answer == "ye" or answer == "yes" or answer == "j" or answer == "ja":
            error = True
            for f in self.faecherarray:
                if self.reviewInProgress[index][3] == f.getShortName():
                    f.addSynomym(self.reviewInProgress[index][2][1:])
                    await m.author.send("**" + self.reviewInProgress[index][2] + "** wurde erfolgreich **"
                                        + self.reviewInProgress[index][3] + "** zugeordnet!")
                    del self.reviewInProgress[index]
                    return
            if error:
                await m.author.send("Es ist ein Fehler aufgetreten!")
                print("Couldn't find matching fach")
                return

        if answer == "n" or answer == "no" or answer == "nein":
            await m.author.send("Vorschlag wurde erfolgreich abgelehnt!")
            del self.reviewInProgress[index]
            return

        await m.author.send("Bitte mit **YES** oder **NO** antworten!")
        return
