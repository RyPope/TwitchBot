__author__ = 'Ryan'
from plugins.BasePlugin import BasePlugin
from database.BaseQueryHelper import BaseQueryHelper

class TestPlugin(BasePlugin):
    def __init__(self, twitchBot):
        super(TestPlugin, self).__init__(twitchBot)
        self.className = self.__class__.__name__
        self.queryHelper = BaseQueryHelper()

        self.registerCommand(self.className, 'channels', self.channelHandler)

    def channelHandler(self, nick, chan, commandArg):
        channels = self.queryHelper.getAllChannels()
        for channel in channels:
            self.sendMessage(self.className, chan, "Channel: %s" % channel.channel)