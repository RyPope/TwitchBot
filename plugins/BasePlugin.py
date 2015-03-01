class BasePlugin(object):
    def __init__(self, twitchBot):
        self.twitchBot = twitchBot

    def _kill(self):
        self.twitchBot = None

    def registerCommand(self, className, command, handler):
        self.twitchBot.registerCommand(className, command, handler)

    def registerAll(self, className, handler):
        self.twitchBot.registerAll(className, handler)

    def registerJoinPartNotifications(self, className, handler):
        self.twitchBot.registerJoinPartNotifications(className, handler)

    def sendMessage(self, className, chan, message, needMod=True):
        self.twitchBot.sendMessage(className, chan, message, needMod)

    def joinChannel(self, channel):
        self.twitchBot.joinChannel(channel)

    def partChannel(self, channel):
        self.twitchBot.partChannel(channel)