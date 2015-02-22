from plugins.BasePlugin import BasePlugin
from plugins.AdPlugin.AdQueryHelper import AdQueryHelper
from util.BaseSettings import Settings
import threading

class AdPlugin(BasePlugin):
    def __init__(self, twitchBot):
        super(AdPlugin, self).__init__(twitchBot)
        self.className = self.__class__.__name__
        self.queryHelper = AdQueryHelper()

        self.registerCommand(self.className, "setad", self.setAdHandler)
        self.registerCommand(self.className, "startads", self.startAdHandler)
        self.registerCommand(self.className, "pauseads", self.pauseAdHandler)

        threading.Timer(10, self.startTimer).start()

    def startAdHandler(self, username, channel, args):
        if not (self.queryHelper.isMod(username, channel or self.queryHelper.isAdmin(username))):
            self.sendMessage(self.className, channel, "You must be a moderator or admin to use this command.")
        else:
            self.queryHelper.setAdEnabled(channel, True)
            self.sendMessage(self.className, channel, "You have started a recurring message")

    def pauseAdHandler(self, username, channel, args):
        if not (self.queryHelper.isMod(username, channel or self.queryHelper.isAdmin(username))):
            self.sendMessage(self.className, channel, "You must be a moderator or admin to use this command.")
        else:
            self.queryHelper.setAdEnabled(channel, False)
            self.sendMessage(self.className, channel, "You have paused a recurring message")

    def startTimer(self):
        advertisements = self.queryHelper.getAllAds()

        for ad in advertisements:
            threading.Timer(int(ad.interval) * 60, self.adMessage, args=(ad.channel_id,)).start()

    def adMessage(self, channel_id):
        advertisement = self.queryHelper.getAdFromID(channel_id)

        threading.Timer(int(advertisement.interval) * 60, self.adMessage, args=(advertisement.channel_id,)).start()
        self.sendMessage(self.className, self.queryHelper.getChannel(advertisement.channel_id), advertisement.message)

    def setAdHandler(self, username, channel, args):
        if len(args) < 3:
            self.sendMessage(self.className, channel, "Invalid syntax, please use startad <interval> <message>")
        elif (not args[1].isdigit()) or (not int(args[1]) % 5 == 0):
            self.sendMessage(self.className, channel, "Interval must be integer of 5 minute increment.")
        elif not (self.queryHelper.isMod(username, channel or self.queryHelper.isAdmin(username))):
            self.sendMessage(self.className, channel, "You must be a moderator or admin to use this command.")
        else:
            self.queryHelper.insertOrUpdateAd(channel, args[1], " ".join(args[2:]))
            self.sendMessage(self.className, channel, "Update advertisement to %s every %s minutes" % (" ".join(args[2:], args[1])))

