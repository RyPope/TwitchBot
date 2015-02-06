from plugins.BasePlugin import BasePlugin
from database.QueryHelper import QueryHelper

class AdminPlugin(BasePlugin):
    def __init__(self, twitchBot):
        super(AdminPlugin, self).__init__(twitchBot)
        self.className = self.__class__.__name__
        self.queryHelper = QueryHelper()

        self.registerCommand(self.className, 'addChannel', self.addChannelHandler)

    def addChannelHandler(self, nick, chan, args):
        if not len(args) == 3:
            self.sendMessage(self.className, chan, "Invalid Syntax, use <channel> <mod>")

        # if self.queryHelper.isAdmin(nick):
            # self.queryHelper.addChannel(args[1], args[2])