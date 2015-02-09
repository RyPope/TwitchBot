from plugins.BasePlugin import BasePlugin
from plugins.AdminPlugin.AdminQueryHelper import AdminQueryHelper

class AdminPlugin(BasePlugin):
    def __init__(self, twitchBot):
        super(AdminPlugin, self).__init__(twitchBot)
        self.className = self.__class__.__name__
        self.queryHelper = AdminQueryHelper()

        self.registerCommand(self.className, 'addchannel', self.addChannelHandler)
        self.registerCommand(self.className, 'removechannel', self.removeChannelHandler)
        self.registerCommand(self.className, 'addmod', self.addModHandler)
        self.registerCommand(self.className, 'removemod', self.removeModHandler)
        self.registerCommand(self.className, 'viewmods', self.viewModsHandler)

    def addChannelHandler(self, nick, chan, args):
        if not len(args) == 3:
            self.sendMessage(self.className, chan, "Invalid Syntax, use addchannel <channel> <mod>")
        elif not self.queryHelper.isAdmin(nick):
            self.sendMessage(self.className, chan, "Only admins may use this command.")
        else:
            self.queryHelper.addChannel(args[1], args[2])
            self.joinChannel(args[1])
            self.sendMessage(self.className, args[1], "Hello! This channel has been added to my list. The current moderator is %s." % args[2])

    def removeChannelHandler(self, nick, chan, args):
        if not len(args) == 2:
            self.sendMessage(self.className, chan, "Invalid Syntax, use removechannel <channel>")
        elif not self.queryHelper.isAdmin(nick):
            self.sendMessage(self.className, chan, "Only admins may use this command.")
        else:
            self.queryHelper.removeChannel(args[1])

    def addModHandler(self, user, chan, args):
        if not len(args) == 2:
            self.sendMessage(self.className, chan, "Invalid Syntax, use addmod <username>")
        elif not (self.queryHelper.isMod(user, chan) or self.queryHelper.isAdmin(user)):
            self.sendMessage(self.className, chan, "Only other channel moderators may use this command.")
        else:
            self.queryHelper.addMod(args[1], chan)
            self.sendMessage(self.className, chan, "Added %s as a moderator to %s" % (args[1], chan))

    def removeModHandler(self, user, chan, args):
        if not len(args) == 2:
            self.sendMessage(self.className, chan, "Invalid Syntax, use removemod <username>")
        elif not (self.queryHelper.isMod(user, chan) or self.queryHelper.isAdmin(user)):
            self.sendMessage(self.className, chan, "Only other channel moderators may use this command.")
        else:
            self.queryHelper.removeMod(args[1], chan)
            self.sendMessage(self.className, chan, "Removed %s as a moderator from %s" % (args[1], chan))

    def viewModsHandler(self, user, chan, args):
        mods = self.queryHelper.viewMods(chan)
        self.sendMessage(self.className, chan, "The mods for %s are %s." % (chan, ", ".join(mods)))