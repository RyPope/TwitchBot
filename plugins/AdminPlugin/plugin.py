from plugins.BasePlugin import BasePlugin
from plugins.AdminPlugin.AdminQueryHelper import AdminQueryHelper
from util.BaseSettings import Settings
import hashlib

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
        self.registerCommand(self.className, 'subscribe', self.betaSignUpHandler)
        self.registerCommand(self.className, 'unsubscribe', self.unsubscribe)
        self.registerCommand(self.className, 'say', self.sayHandler)
        self.registerCommand(self.className, 'donate', self.donateHandler)
        self.registerCommand(self.className, 'bug', self.bugHandler)
        self.registerCommand(self.className, 'contact', self.contactHandler)

        self.registerAll(self.className, self.commandHandler)

    def bugHandler(self, username, channel, args):
        if len(args) < 2:
            self.sendMessage(self.className, channel, "All bug reports are appreciated! Please use report <issue description> to file a bug report.")
        else:
            self.sendMessage(self.className, channel, "Thank you for your bug report.");
            self.queryHelper.logBug(username, channel, " ".join(args[1:]))

    def contactHandler(self, username, channel, args):
        if len(args) < 2:
            self.sendMessage(self.className, channel, "To write a message for the admins please use contact <message>.")
        else:
            self.sendMessage(self.className, channel, "Your message has been sent.");
            self.queryHelper.logMail(username, channel, " ".join(args[1:]))

    def donateHandler(self, username, channel, args):
        self.sendMessage(self.className, channel, "If you enjoy the use of this bot please feel free to either follow the developer at twitch.tv/PopeTheThird or donate at twitchalerts.com/donate/popethethird. All are appreciated! Bitcoin accepted at 15KCMc2swEeqdmcx1UjCyWVLeUsJsxc9xx.")

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
            self.partChannel(args[1])
            self.queryHelper.removeChannel(args[1])

    def addModHandler(self, user, chan, args):
        if not len(args) == 2:
            self.sendMessage(self.className, chan, "Invalid Syntax, use addmod <username>")
        elif not (self.queryHelper.isMod(user, chan) or self.queryHelper.isAdmin(user)):
            self.sendMessage(self.className, chan, "Only other channel moderators may use this command.")
        else:
            self.queryHelper.addMod(args[1], chan)
            self.sendMessage(self.className, chan, "Added %s as a moderator to %s" % (args[1], chan))

    def sayHandler(self, user, chan, args):
        if len(args) < 2:
            self.sendMessage(self.className, chan, "Invalid Syntax, use say <message>")
        elif not (self.queryHelper.isAdmin(user)):
            self.sendMessage(self.className, chan, "Only admins may use this command.")
        else:
            self.sendMessage(self.className, chan, " ".join(args[1:]), False)

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

    def unsubscribe(self, username, channel, args):
        m = hashlib.md5()
        m.update(channel)
        if len(args) < 2:
            self.sendMessage(self.className, channel, "To have this bot leave your channel please use \"unsubscribe %s\". All your settings and logs will be retained if you wish to subscribe again. Thanks!" % (m.hexdigest(),))
        elif not (self.queryHelper.isMod(username, channel) or self.queryHelper.isAdmin(username)):
            self.sendMessage(self.className, channel, "Only channel moderators may use this command.")
        else:
            if args[1] == m.hexdigest():
                self.queryHelper.removeChannel(channel)
                self.sendMessage(self.className, channel, "Good-bye!")
                self.partChannel(channel)

    def betaSignUpHandler(self, user, chan, args):
        self.queryHelper.addChannel("#%s" % user, user, True)
        self.sendMessage(self.className, chan, "Signed up. This bot will join your stream channel shortly. It can be removed by using unsubscribe in your channel.")

