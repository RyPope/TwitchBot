from plugins.BasePlugin import BasePlugin
from database.QueryHelper import QueryHelper

class TestPlugin(BasePlugin):
    def __init__(self, twitchBot):
        super(TestPlugin, self).__init__(twitchBot)
        self.queryHelper = QueryHelper()

        self.registerCommand('channels', self.channelHandler)

    def channelHandler(self, nick, chan, commandArg):
        channels = self.queryHelper.getAllChannels()
        for channel in channels:
            self.sendMessage(chan, "Channel: %s" % channel.channel)