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

    def sendMessage(self, className, chan, message):
        self.twitchBot.sendMessage(className, chan, message)

    def joinChannel(self, channel):
        self.twitchBot.joinChannel(channel)