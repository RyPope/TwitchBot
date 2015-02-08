from plugins.BasePlugin import BasePlugin
from database.BaseQueryHelper import BaseQueryHelper

class SpamPlugin(BasePlugin):
    def __init__(self, twitchBot):
        super(SpamPlugin, self).__init__(twitchBot)
        self.className = self.__class__.__name__
        self.queryHelper = BaseQueryHelper()

        self.registerAll(self.className, self.msgHandler)
        self.registerCommand(self.className, "addSpam", self.addSpam)
        self.registerCommand(self.className, "removeSpam", self.removeSpam)

    def msgHandler(self, nick, chan, msg):
        pass

    def addSpam(self, nick, chan, args):
        pass

    def removeSpam(self, nick, chan, args):
        pass

