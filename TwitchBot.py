__author__ = 'Ryan'

import socket
import time
import imp
import os
import traceback
import re
import inspect
from threading import Thread
from plugins.BasePlugin import BasePlugin
from util.BaseSettings import Settings
from database.BaseQueryHelper import BaseQueryHelper

class TwitchBot:
    def __init__(self):
        self.ircSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc_host = Settings.irc_host
        self.irc_chan = '#' + Settings.irc_channel.lower()
        self.connected = False
        self._pluginFolder = './plugins/'
        self._mainModule = 'plugin'
        self._plugins = []
        self.commands = []
        self.msgRegister = []
        self.joinPartHandlers = []
        self.loadedPluginNames = []
        self.moddedInList = []

        self.queryHelper = BaseQueryHelper()

    def kill(self):
        for p in self._plugins:
            p._kill()

    def sendMessage(self, className, chan, message, needMod=True):
        # if (needMod and chan in self.moddedInList) or (not needMod):
            self.ircSock.send(str('PRIVMSG %s :%s\n' % (chan, message)).encode('UTF-8'))
        # else:
        #     print("Channel %s attempted to use commands without modding bot" % chan)



    def connect(self, port):
        self.ircSock.connect((self.irc_host, port))
        self.ircSock.send(str("Pass " + Settings.irc_oauth + "\r\n").encode('UTF-8'))
        self.ircSock.send(str("NICK " + Settings.irc_username + "\r\n").encode('UTF-8'))

        for channel in self.queryHelper.getAllChannels():
            if self.queryHelper.channelIsEnabled(channel.channel.lower()):
                self.joinChannel(channel.channel.lower())
                time.sleep(.5)

    def joinChannel(self, channel):
        self.ircSock.send(str("JOIN " + channel.lower() + "\r\n").encode('UTF-8'))

    def leaveChannel(self, channel):
        self.ircSock.send(str("PART " + channel.lower() + "\r\n").encode('UTF-8'))

    def registerCommand(self, className, command, pluginFunction):
        self.commands.append( {'regex': command, 'handler':pluginFunction, 'plugin':className} )

    def registerAll(self, className, pluginFunction):
        self.msgRegister.append( {'handler':pluginFunction, 'plugin':className} )

    def registerJoinPartNotifications(self, className, pluginFunction):
        self.joinPartHandlers.append( { 'handler':pluginFunction, 'plugin':className } )

    def handleIRCMessage(self, ircMessage):
        nick = ircMessage.split('!')[0][1:]

        # Message to a channel
        if ircMessage.find(' PRIVMSG #') != -1:
            chan = ircMessage.split(' ')[2]
            msg = ircMessage.split(' PRIVMSG ' + chan + ' :')[1]

            for pluginDict in self.commands:
                if re.search('^' + Settings.irc_trigger + pluginDict['regex'], msg, re.IGNORECASE) \
                        and not self.queryHelper.checkPluginDisabled(chan, pluginDict['plugin']):
                    handler = pluginDict['handler']
                    args = msg.split(" ")
                    handler(nick, chan, args)

            for pluginDict in self.msgRegister:
                if not self.queryHelper.checkPluginDisabled(chan, pluginDict['plugin']):
                    handler = pluginDict['handler']
                    args = msg.split(" ")
                    handler(nick, chan, args)

        # User joined channel
        elif ircMessage.find('JOIN ') != -1:
            nick = ircMessage.split('!')[0][1:]
            chan = ircMessage.split(' ')[2]

            print(nick + " joined " + chan)
            for handler in self.joinPartHandlers:
                if not self.queryHelper.checkPluginDisabled(chan, handler['plugin']):
                    handler['handler'](nick, chan, True)

        # User left channel
        elif ircMessage.find('PART ') != -1:
            nick = ircMessage.split('!')[0][1:]
            chan = ircMessage.split(' ')[2]

            print(nick + " left " + chan)
            for handler in self.joinPartHandlers:
                if not self.queryHelper.checkPluginDisabled(chan, handler['plugin']):
                    handler['handler'](nick, chan, False)

        # # User oped in channel
        elif ircMessage.find('MODE ') != -1:
            nick = ircMessage.split(' ')[-1]
            chan = ircMessage.split(' ')[2]
            op = ircMessage.split(' ')[3]

            if nick.lower() == Settings.irc_username.lower():
                if op == "+o" and not chan in self.moddedInList:
                    self.moddedInList.append(chan)
                    print("Modded in %s" % chan)
                elif op == "-o" and chan in self.moddedInList:
                    self.moddedInList.remove(chan)
                    print("Unmodded in %s" % chan)
        else:
            pass

    def run(self):
        line_sep_exp = re.compile(b'\r?\n')
        socketBuffer = b''
        while True:
            try:
                self.connected = True
                socketBuffer += self.ircSock.recv(1024)

                ircMsgs = line_sep_exp.split(socketBuffer)

                socketBuffer = ircMsgs.pop()

                for ircMsg in ircMsgs:
                    msg = ircMsg.decode('utf-8')
                    Thread(target=self.handleIRCMessage, args=(msg,)).start()
            except:
                raise

    def loadPlugins(self):
        potentialPlugins = []
        allPlugins = os.listdir(self._pluginFolder)
        for i in allPlugins:
            location = os.path.join(self._pluginFolder, i)
            if not os.path.isdir(location) or not self._mainModule + ".py" in os.listdir(location):
                continue
            info = imp.find_module(self._mainModule, [location])
            potentialPlugins.append({"name": i, "info": info})

        print("Found plugin classes:")
        for i in potentialPlugins:
            try:
                plugin = imp.load_module(self._mainModule, *i["info"])
                pluginClasses = inspect.getmembers(plugin, inspect.isclass)
                for className, classObj in pluginClasses:
                    if className == "BasePlugin" or className in self.loadedPluginNames or not issubclass(classObj, BasePlugin):
                        continue
                    print(className)
                    pluginInstance = classObj(self)
                    self._plugins.append(pluginInstance)
                    self.loadedPluginNames.append(className)
            except Exception as e:
                print("Error loading plugin.")
                print(traceback.format_exc())

if __name__ == "__main__":
    while True:
        twitchBot = TwitchBot()
        try:
            twitchBot.loadPlugins()
            twitchBot.connect(6667)
            twitchBot.run()
        except Exception as e:
            print(traceback.format_exc())
        twitchBot.kill()
        time.sleep(5)
