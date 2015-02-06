from plugins.BasePlugin import BasePlugin
from plugins.LoggingPlugin.QueryHelper import QueryHelper

class LoggingPlugin(BasePlugin):
    def __init__(self, twitchBot):
        super(LoggingPlugin, self).__init__(twitchBot)
        self.className = self.__class__.__name__
        self.queryHelper = QueryHelper()

        self.registerAll(self.className, self.messageHandler)
        self.registerForJoinPartNotifications(self.className, self.joinPartHandler)

    def messageHandler(self, username, channel, msg):
        pass

    def joinPartHandler(self, username, channel, isJoin):
        self.queryHelper.insertUser(username)