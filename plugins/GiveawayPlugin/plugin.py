from plugins.BasePlugin import BasePlugin
from plugins.GiveawayPlugin.GiveawayQueryHelper import GiveawayQueryHelper
from collections import defaultdict
from random import randint
from objects.entry import Entry

class GiveawayPlugin(BasePlugin):
    def __init__(self, twitchBot):
        super(GiveawayPlugin, self).__init__(twitchBot)
        self.className = self.__class__.__name__
        self.queryHelper = GiveawayQueryHelper()

        self.currentUsers = defaultdict(list)
        self.currentSingleGiveaways = defaultdict(list)
        self.currentPointsGiveaways = defaultdict(list)

        # giveaway <type (single, all, points)>
        #   giveaway type points <optional: minimum>
        # endgiveaway
        # enter <optional: points>

        self.registerCommand(self.className, "giveaway", self.giveawayHandler)
        self.registerCommand(self.className, "enter", self.enterGiveaway)
        self.registerCommand(self.className, "endgiveaway", self.endGiveaway)
        self.registerJoinPartNotifications(self.className, self.joinPartHandler)

    def joinPartHandler(self, username, channel, isJoin):
        if isJoin:
            self.currentUsers[channel].append(username)
        else:
            if username in self.currentUsers[channel]:
                self.currentUsers[channel].remove(username)

    def giveawayHandler(self, username, channel, args):
        if len(args) < 2:
            self.sendMessage(self.className, channel, "Invalid syntax, please use giveaway <single | all | points>")
        elif not (args[1].lower() == "single" or args[1].lower() == "all" or args[1].lower() == "points"):
            self.sendMessage(self.className, channel, "Invalid syntax, please use giveaway <single | all | points>")
        elif not (self.queryHelper.isMod(username, channel) or self.queryHelper.isAdmin(username)):
            self.sendMessage(self.className, channel, "You must be a moderator or admin to use this command.")
        else:
            command = args[1].encode("UTF-8").lower()

            if command == "all":
                self.giveawayAll(channel)
            elif command == "single":
                self.giveawaySingle(channel)
            elif command == "points":
                self.giveawayPoints(channel)

    def giveawaySingle(self, channel):
        if not len(self.currentSingleGiveaways[channel]) == 0 or not len(self.currentPointsGiveaways[channel]) == 0:
            self.sendMessage(self.className, channel, "There is a current giveaway in progress. Type !enter to enter.")
        else:
            self.currentSingleGiveaways[channel].append("")
            self.sendMessage(self.className, channel, "You have started a giveaway. Anyone may enter using !enter.")

    def giveawayPoints(self, channel):
        if not (len(self.currentSingleGiveaways[channel]) == 0 or len(self.currentPointsGiveaways[channel]) == 0):
            self.sendMessage(self.className, channel, "There is a current giveaway in progress. Type !enter to enter.")
        else:
            self.currentPointsGiveaways[channel].append(Entry("", "", 0))
            self.sendMessage(self.className, channel, "You have started a giveaway. Anyone may enter using !enter <points>.")

    def enterGiveaway(self, username, channel, args):
        if len(self.currentSingleGiveaways[channel]) == 0 and len(self.currentPointsGiveaways[channel]) == 0:
            self.sendMessage(self.className, channel, "There are no current giveaways.")
        else:
            if not len(self.currentSingleGiveaways[channel]) == 0:
                if username in self.currentSingleGiveaways[channel]:
                    self.sendMessage(self.className, channel, "You have already signed up for this giveaway.")
                else:
                    self.currentSingleGiveaways[channel].append(username)
                    self.sendMessage(self.className, channel, "You have been signed up for this giveaway. Current entries: %s"
                                     % (len(self.currentSingleGiveaways[channel]) - 1))
            elif not len(self.currentPointsGiveaways[channel]) == 0:
                users = [x for x in self.currentPointsGiveaways[channel] if str(x.username) == str(username) and str(x.channel) == str(channel)]
                if not len(users) == 0:
                    self.sendMessage(self.className, channel, "You have already signed up for this giveaway.")
                elif len(args) < 2:
                    self.sendMessage(self.className, channel, "Must specify point value, use enter <points>")
                elif not args[1].isdigit() or int(args[1]) <= 0:
                    self.sendMessage(self.className, channel, "Point value must be positive integer.")
                elif int(args[1]) > self.queryHelper.getPoints(username, channel):
                    self.sendMessage(self.className, channel, "You do not have sufficient points.")
                else:
                    points = int(args[1])
                    self.currentPointsGiveaways[channel].append(Entry(username, channel, points))
                    self.sendMessage(self.className, channel, "You have been signed up for this giveaway. Current entries: %s"
                                     % (len(self.currentPointsGiveaways[channel]) - 1))

                    self.queryHelper.deductPoints(username, channel, points)

    def endGiveaway(self, username, channel, args):
        if not (self.queryHelper.isMod(username, channel) or self.queryHelper.isAdmin(username)):
            self.sendMessage(self.className, channel, "You must be a moderator or admin to use this command.")
        elif len(self.currentSingleGiveaways[channel]) > 0:
            max = len(self.currentSingleGiveaways[channel])
            rand = randint(1, max - 1)
            self.sendMessage(self.className, channel, "Picked: %s!" % self.currentSingleGiveaways[channel][rand])
            self.currentSingleGiveaways[channel] = []

        elif len(self.currentPointsGiveaways[channel]) > 0:
            total = self.countEntries(self.currentPointsGiveaways[channel])
            rand = randint(1, total)
            entry = self.getEntryAt(self.currentPointsGiveaways[channel], rand)

            self.sendMessage(self.className, channel, "Picked: %s!" % entry.username)
            self.currentPointsGiveaways[channel] = []

    def giveawayAll(self, channel):
        max = len(self.currentUsers[channel])
        rand = randint(1, max - 1)
        self.sendMessage(self.className, channel, "Picked: %s!" % self.currentUsers[channel][rand])

    def getEntryAt(self, entries, num):
        curr = 0
        for entry in entries:
            curr += entry.points

            if curr >= num:
                return entry

        assert "Did not find entry..."
        return None

    def countEntries(self, entries):
        total = 0
        for entry in entries:
            total += entry.points

        return total