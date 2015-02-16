from plugins.BasePlugin import BasePlugin
from plugins.AdminPlugin.AdminQueryHelper import AdminQueryHelper
from util.BaseSettings import Settings

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
        self.registerCommand(self.className, 'addcommand', self.addCommandHandler)
        self.registerCommand(self.className, 'removecommand', self.removeCommandHandler)
        self.registerCommand(self.className, 'commands', self.viewCommandsHandler)
        self.registerCommand(self.className, 'signup', self.betaSignUpHandler)

        self.registerAll(self.className, self.commandHandler)

    def addChannelHandler(self, nick, chan, args):
        if not len(args) == 3:
            self.sendMessage(self.className, chan, "Invalid Syntax, use addchannel <channel> <mod>")
        elif not self.queryHelper.isAdmin(nick):
            self.sendMessage(self.className, chan, "Only admins may use this command.")
        else:
            self.queryHelper.addChannel(args[1], args[2])
            self.joinChannel(args[1])
            self.sendMessage(self.className, args[1],
                             """Hello! This channel has been added to my list. The current moderator is %s.
                             To prevent rate limiting I will only be able to communicate if I am added as a mod.""" % (args[2]),
                             False)

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

    def addCommandHandler(self, user, chan, args):
        if len(args) < 3:
            self.sendMessage(self.className, chan, "Invalid Syntax, use addcommand <trigger> <output>")
        elif not (self.queryHelper.isMod(user, chan) or self.queryHelper.isAdmin(user)):
            self.sendMessage(self.className, chan, "Only channel moderators may use this command.")
        else:
            self.queryHelper.addCommand(chan, args[1].lower(), " ".join(args[2:]))
            self.sendMessage(self.className, chan, "Added command '%s'" % args[1])

    def removeCommandHandler(self, user, chan, args):
        if len(args) < 2:
            self.sendMessage(self.className, chan, "Invalid Syntax, use removecommand <trigger>")
        elif not (self.queryHelper.isMod(user, chan) or self.queryHelper.isAdmin(user)):
            self.sendMessage(self.className, chan, "Only channel moderators may use this command.")
        else:
            self.queryHelper.removeCommand(chan, args[1].lower())
            self.sendMessage(self.className, chan, "Removed command '%s'" % args[1])

    def viewCommandsHandler(self, user, chan, args):
        commands = self.queryHelper.viewCommands(chan)
        self.sendMessage(self.className, chan, "The commands for %s are %s." % (chan, ", ".join(commands)))

    def commandHandler(self, user, chan, args):
        if args[0][0] == Settings.irc_trigger:
            key = args[0][1:]
            value = self.queryHelper.getCommand(chan, key)

            if not value is None:
                self.sendMessage(self, chan, value)

    def betaSignUpHandler(self, user, chan, args):
        self.queryHelper.addChannel("#%s" % user, user, False)
        self.sendMessage(self.className, chan, "Signed up for beta. This bot will join your stream channel when beta begins.")

