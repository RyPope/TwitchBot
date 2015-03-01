from plugins.BasePlugin import BasePlugin
from plugins.AdPlugin.AdQueryHelper import AdQueryHelper
from util.BaseSettings import Settings
import threading

class AdPlugin(BasePlugin):
    def __init__(self, twitchBot):
        super(AdPlugin, self).__init__(twitchBot)
        self.className = self.__class__.__name__
        self.queryHelper = AdQueryHelper()

        self.registerCommand(self.className, "ad", self.setAdHandler)

        threading.Timer(10, self.startTimer).start()

    def startTimer(self):
        advertisements = self.queryHelper.getAllAds()

        for ad in advertisements:
            threading.Timer(int(ad.interval) * 60, self.adMessage, args=(ad.channel_id,)).start()

    def adMessage(self, channel_id):
        advertisement = self.queryHelper.getAdFromID(channel_id)

        threading.Timer(int(advertisement.interval) * 60, self.adMessage, args=(advertisement.channel_id,)).start()
        self.sendMessage(self.className, self.queryHelper.getChannel(advertisement.channel_id), advertisement.message)

    def setAdHandler(self, username, channel, args):
        if len(args) < 2:
            self.sendMessage(self.className, channel, "Invalid syntax, please use ad <start | pause | set>")
        elif args[1].lower() == "set":
            if len(args) < 3:
                self.sendMessage(self.className, channel, "Invalid syntax, please use setad <interval> <message>")
            elif (not args[2].isdigit()) or (not int(args[2]) % 5 == 0):
                self.sendMessage(self.className, channel, "Interval must be integer of 5 minute increment.")
            elif not (self.queryHelper.isMod(username, channel or self.queryHelper.isAdmin(username))):
                self.sendMessage(self.className, channel, "You must be a moderator or admin to use this command.")
            else:
                self.queryHelper.insertOrUpdateAd(channel, args[2], " ".join(args[3:]))
                self.sendMessage(self.className, channel, "Update advertisement to %s every %s minutes" % (" ".join(args[3:], args[2])))
        elif args[1].lower() == "start":
            if not (self.queryHelper.isMod(username, channel) or self.queryHelper.isAdmin(username)):
                self.sendMessage(self.className, channel, "You must be a moderator or admin to use this command.")
            else:
                self.queryHelper.setAdEnabled(channel, True)
                self.sendMessage(self.className, channel, "You have started a recurring message")
        elif args[1].lower() == "pause":
            if not (self.queryHelper.isMod(username, channel) or self.queryHelper.isAdmin(username)):
                self.sendMessage(self.className, channel, "You must be a moderator or admin to use this command.")
            else:
                self.queryHelper.setAdEnabled(channel, False)
                self.sendMessage(self.className, channel, "You have paused a recurring message")
