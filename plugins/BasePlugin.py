class BasePlugin(object):
    def __init__(self, twitchy):
        self.twitchy = twitchy

    def _kill(self):
        self.twitchy = None

    def registerCommand(self, className, command, handler):
        self.twitchy.registerCommand(className, command, handler)

    def registerAll(self, className, handler):
        self.twitchy.registerAll(className, handler)

    def registerForJoinPartNotifications(self, className, handler):
        self.twitchy.registerForJoinPartNotifications(className, handler)

    def sendMessage(self, className, chan, message):
        self.twitchy.sendMessage(className, chan, message)
