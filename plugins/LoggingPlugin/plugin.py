from plugins.BasePlugin import BasePlugin
from plugins.LoggingPlugin.LoggingQueryHelper import LoggingQueryHelper

class LoggingPlugin(BasePlugin):
    def __init__(self, twitchBot):
        super(LoggingPlugin, self).__init__(twitchBot)
        self.className = self.__class__.__name__
        self.loggingQueryHelper = LoggingQueryHelper()

        self.registerAll(self.className, self.messageHandler)
        self.registerJoinPartNotifications(self.className, self.joinPartHandler)

    def messageHandler(self, username, channel, args):
        self.loggingQueryHelper.insertMsg(username, channel, " ".join(args))

    def joinPartHandler(self, username, channel, isJoin):
        self.loggingQueryHelper.insertUser(username)