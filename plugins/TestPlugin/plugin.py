from plugins.BasePlugin import BasePlugin
from database.QueryHelper import QueryHelper

class TestPlugin(BasePlugin):
    def __init__(self, twitchBot):
        super(TestPlugin, self).__init__(twitchBot)
        self.className = self.__class__.__name__
        self.queryHelper = QueryHelper()

        self.registerCommand(self.className, 'channels', self.channelHandler)
        self.registerCommand(self.className, 'enabled', self.enabledPlugin)

    def channelHandler(self, nick, chan, commandArg):
        channels = self.queryHelper.getAllChannels()
        for channel in channels:
            self.sendMessage(self.className, chan, "Channel: %s" % channel.channel)

    def enabledPlugin(self, nick, chan, commandArg):
        enabled = self.queryHelper.checkPluginEnabled(chan, commandArg[1])
        self.sendMessage(self.className, chan, "Plugin %s enabled: %s" % (commandArg[1], str(enabled)) )