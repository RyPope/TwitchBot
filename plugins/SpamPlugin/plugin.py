from plugins.BasePlugin import BasePlugin
from plugins.SpamPlugin.SpamQueryHelper import SpamQueryHelper

class SpamPlugin(BasePlugin):
    def __init__(self, twitchBot):
        super(SpamPlugin, self).__init__(twitchBot)
        self.className = self.__class__.__name__
        self.queryHelper = SpamQueryHelper()

        self.registerAll(self.className, self.msgHandler)
        self.registerCommand(self.className, "addspam", self.addSpam)
        self.registerCommand(self.className, "removespam", self.removeSpam)
        self.registerCommand(self.className, "viewspam", self.viewSpam)
        self.registerCommand(self.className, "prohibitlinks", self.prohibitLinksHandler)
        self.registerCommand(self.className, "allowlinks", self.allowLinksHandler)

    def msgHandler(self, user, chan, msg):
        inputStr = " ".join(msg)
        if "www." in inputStr or "http://" in inputStr or "https://" in inputStr:
            self.sendMessage(self.className, chan, "URL Detected")

    def addSpam(self, user, chan, args):
        if len(args) < 2:
            self.sendMessage(self.className, chan, "Invalid Syntax, use addspam <spam words>")
        elif not (self.queryHelper.isMod(user, chan) or self.queryHelper.isAdmin(user)):
            self.sendMessage(self.className, chan, "Only channel moderators may use this command.")
        else:
            self.queryHelper.addSpam(chan, " ".join(args[1:]).lower())
            self.sendMessage(self.className, chan, "Added '%s' to spam filter." % " ".join(args[1:]).lower())

    def removeSpam(self, user, chan, args):
        if len(args) < 2:
            self.sendMessage(self.className, chan, "Invalid Syntax, use removespam <spam word>")
        elif not (self.queryHelper.isMod(user, chan) or self.queryHelper.isAdmin(user)):
            self.sendMessage(self.className, chan, "Only channel moderators may use this command.")
        else:
            self.queryHelper.removeSpam(chan, " ".join(args[1:]).lower())
            self.sendMessage(self.className, chan, "Removed '%s' from spam filter." % " ".join(args[1:]).lower())

    def viewSpam(self, user, chan, args):
        if not (self.queryHelper.isMod(user, chan) or self.queryHelper.isAdmin(user)):
            self.sendMessage(self.className, chan, "Only channel moderators may use this command.")
        else:
            spamMessages = self.queryHelper.getSpam(chan)
            self.sendMessage(self.className, chan, "Your current prohibited messages are: " + ", ".join(spamMessages))

    def prohibitLinksHandler(self, user, chan, args):
        if not (self.queryHelper.isMod(user, chan) or self.queryHelper.isAdmin(user)):
            self.sendMessage(self.className, chan, "Only channel moderators may use this command.")
        else:
            self.queryHelper.prohibitLinks(chan)
            self.sendMessage(self.className, chan, "Posting links is now prohibited for non-moderators.")

    def allowLinksHandler(self, user, chan, args):
        if not (self.queryHelper.isMod(user, chan) or self.queryHelper.isAdmin(user)):
            self.sendMessage(self.className, chan, "Only channel moderators may use this command.")
        else:
            self.queryHelper.allowLinks(chan)
            self.sendMessage(self.className, chan, "Posting links is now allowed for all users.")
