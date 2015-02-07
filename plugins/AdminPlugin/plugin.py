from plugins.BasePlugin import BasePlugin
from database.BaseQueryHelper import QueryHelper

class AdminPlugin(BasePlugin):
    def __init__(self, twitchBot):
        super(AdminPlugin, self).__init__(twitchBot)
        self.className = self.__class__.__name__
        self.queryHelper = QueryHelper()

        self.registerCommand(self.className, 'addchannel', self.addChannelHandler)
        self.registerCommand(self.className, 'removechannel', self.removeChannelHandler)

    def addChannelHandler(self, nick, chan, args):
        if not len(args) == 3:
            self.sendMessage(self.className, chan, "Invalid Syntax, use <channel> <mod>")
        elif not self.queryHelper.isAdmin(nick):
            self.sendMessage(self.className, chan, "Only admins may use this command.")
        else:
            self.queryHelper.addChannel(args[1], args[2])

    def removeChannelHandler(self, nick, chan, args):
        if not len(args) == 2:
            self.sendMessage(self.className, chan, "Invalid Syntax, use <channel>")
        elif not self.queryHelper.isAdmin(nick):
            self.sendMessage(self.className, chan, "Only admins may use this command.")
        else:
            self.queryHelper.removeChannel(args[1])


