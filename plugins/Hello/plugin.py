from plugins.BasePlugin import BasePlugin


class HelloPlugin(BasePlugin):
    def __init__(self, twitchBot):
        super(HelloPlugin, self).__init__(twitchBot)

        self.registerCommand('hello', self.helloHandler)
        self.registerTrigger('hey', self.heyHandler)

        self.registerForJoinPartNotifications(self.userJoinPart)
        self.registerForModNotifications(self.modGivenTaken)

    def helloHandler(self, nick, commandArg):
        self.sendMessage("Hello " + nick + "!")

    def heyHandler(self, nick, fullMsg):
        self.sendMessage("Hey there, " + nick)

    def userJoinPart(self, nick, isJoining):
        if isJoining:
            self.sendMessage("Welcome " + nick + "!")
        else:
            self.sendMessage("See ya, " + nick)

    def modGivenTaken(self, nick, modGiven):
        if modGiven:
            self.sendMessage("Run! " + nick + " has been given moderator powers!")
        else:
            self.sendMessage("Relax, " + nick + " has lost moderator powers")
