from plugins.BasePlugin import BasePlugin
from plugins.LoggingPlugin.LoggingQueryHelper import LoggingQueryHelper
import datetime

class LoggingPlugin(BasePlugin):
    def __init__(self, twitchBot):
        super(LoggingPlugin, self).__init__(twitchBot)
        self.className = self.__class__.__name__
        self.loggingQueryHelper = LoggingQueryHelper()

        self.registerAll(self.className, self.messageHandler)
        self.registerJoinPartNotifications(self.className, self.joinPartHandler)
        self.registerCommand(self.className, "stats", self.myStatsHandler)
        self.registerCommand(self.className, "testpart", self.testPartHandler)

        self.joinList = []

    def testPartHandler(self, username, channel, args):
        joinTime = self.loggingQueryHelper.popJoined(username, channel)
        diff = datetime.datetime.now() - joinTime
        timeSpent = divmod(diff.days * 86400 + diff.seconds, 60)
        self.loggingQueryHelper.updateTimeSpent(username, channel, timeSpent[0])
        print(self.className, channel, "%s spent %d minutes, %d seconds in %s" % (username, timeSpent[0], timeSpent[1], channel))

    def messageHandler(self, username, channel, args):
        self.loggingQueryHelper.insertMsg(username, channel, " ".join(args))

    def joinPartHandler(self, username, channel, isJoin):
        self.loggingQueryHelper.insertUser(username)

        if isJoin:
            self.loggingQueryHelper.insertJoined(username, channel, datetime.datetime.now())
        else:
            joinTime = self.loggingQueryHelper.popJoined(username, channel)
            diff = datetime.datetime.now() - joinTime
            timeSpent = divmod(diff.days * 86400 + diff.seconds, 60)
            self.loggingQueryHelper.updateTimeSpent(username, channel, timeSpent[0])
            print(self.className, channel, "%s spent %d minutes, %d seconds in %s" % (username, timeSpent[0], timeSpent[1], channel))

    def myStatsHandler(self, username, channel, args):
        chatMessages = self.loggingQueryHelper.getMessages(username, channel)
        numChars = 0
        for message in chatMessages:
            numChars += len(message.message)

        self.sendMessage(self.className, channel, "You have sent %d messages (%d characters) to channel %s" % (len(chatMessages), numChars, channel))