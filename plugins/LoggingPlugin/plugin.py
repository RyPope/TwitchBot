from plugins.BasePlugin import BasePlugin
from plugins.LoggingPlugin.LoggingQueryHelper import LoggingQueryHelper

class LoggingPlugin(BasePlugin):
    def __init__(self, twitchBot):
        super(LoggingPlugin, self).__init__(twitchBot)
        self.className = self.__class__.__name__
        self.loggingQueryHelper = LoggingQueryHelper()

        self.registerAll(self.className, self.messageHandler)
        self.registerJoinPartNotifications(self.className, self.joinPartHandler)
        self.registerCommand(self.className, "mystats", self.myStatsHandler)

    def messageHandler(self, username, channel, args):
        self.loggingQueryHelper.insertMsg(username, channel, " ".join(args))

    def joinPartHandler(self, username, channel, isJoin):
        self.loggingQueryHelper.insertUser(username)

    def myStatsHandler(self, username, channel, args):
        chatMessages = self.loggingQueryHelper.getMessages(username, channel)
        numChars = 0
        for message in chatMessages:
            numChars += len(message.message)

        self.sendMessage(self.className, channel, "You have sent %d messages (%d characters) to channel %s" % (len(chatMessages), numChars, channel))