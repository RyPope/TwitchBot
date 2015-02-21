from plugins.BasePlugin import BasePlugin
from plugins.LoggingPlugin.LoggingQueryHelper import LoggingQueryHelper
from collections import defaultdict
import threading

class LoggingPlugin(BasePlugin):
    def __init__(self, twitchBot):
        super(LoggingPlugin, self).__init__(twitchBot)
        self.className = self.__class__.__name__
        self.loggingQueryHelper = LoggingQueryHelper()

        self.currentUsers = defaultdict(list)
        self.toUpdate = defaultdict(list)

        self.registerAll(self.className, self.messageHandler)
        self.registerJoinPartNotifications(self.className, self.joinPartHandler)
        self.registerCommand(self.className, "stats", self.myStatsHandler)

        self.updateTimeSpent()

    def updateTimeSpent(self):
        threading.Timer(60, self.updateTimeSpent).start()

        for channel, values in self.toUpdate.items():
            for username in values:
                self.loggingQueryHelper.updateTimeSpent(username, channel, 1)

        self.toUpdate = self.currentUsers

    def messageHandler(self, username, channel, args):
        self.loggingQueryHelper.insertMsg(username, channel, " ".join(args))

    def joinPartHandler(self, username, channel, isJoin):
        self.loggingQueryHelper.insertUser(username)

        if isJoin:
            self.currentUsers[channel].append(username)
        else:
            if username in self.currentUsers[channel]:
                self.currentUsers[channel].remove(username)


    def myStatsHandler(self, username, channel, args):
        chatMessages = self.loggingQueryHelper.getMessages(username, channel)
        numChars = 0
        for message in chatMessages:
            numChars += len(message.message)

        minutes = self.loggingQueryHelper.getPoints(username, channel)
        self.sendMessage(self.className, channel, "You have sent %d messages (%d characters) and spent %s minutes in chat." % (len(chatMessages), numChars, minutes))