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

class TwitchBot:
    def __init__(self):
        self.ircSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ircServ = Settings.IRC_Server
        self.ircChan = '#'+ Settings.Twitch_Channel.lower()

        self.connected = False
        self._pluginFolder = './plugins/'
        self._mainModule = 'plugin'
        self._plugins = []
        self.commands = []
        self.triggers = []
        self.joinPartHandlers = []
        self.modHandlers = []
        self.ignoredUsers = []
        self.loadedPluginNames = []
        self.spamMessages = ['codes4free.net', 'g2a.com/r/', 'prizescode.net']

    def kill(self):
        for p in self._plugins:
            p._kill()

    def sendMessage(self, message):
        self.ircSock.send(str('PRIVMSG %s :%s\n' % (self.ircChan, message)).encode('UTF-8'))

    def connect(self, port):
        self.ircSock.connect((self.ircServ, port))
        self.ircSock.send(str("Pass " + Settings.Twitch_Password + "\r\n").encode('UTF-8'))
        self.ircSock.send(str("NICK " + Settings.Twitch_Username + "\r\n").encode('UTF-8'))
        self.ircSock.send(str("JOIN " + self.ircChan + "\r\n").encode('UTF-8'))

    def loadPlugins(self):
        potentialPlugins = []
        allplugins = os.listdir(self._pluginFolder)
        for i in allplugins:
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

    def registerCommand(self, command, pluginFunction):
        self.commands.append( {'regex': command, 'handler':pluginFunction} )

    def registerTrigger(self, trigger, pluginFunction):
        self.triggers.append( {'regex': trigger, 'handler':pluginFunction} )

    def registerForJoinPartNotifications(self, pluginFunction):
        self.joinPartHandlers.append( pluginFunction )

    def registerForModNotifications(self, pluginFunction):
        self.modHandlers.append( pluginFunction )

    def handleIRCMessage(self, ircMessage):
        if ircMessage.find(' PRIVMSG '+ self.ircChan +' :') != -1:
            nick = ircMessage.split('!')[0][1:]
            if nick.lower() in self.ignoredUsers:
                return
            msg = ircMessage.split(' PRIVMSG '+ self.ircChan +' :')[1]

            if re.search('^%signore' % Settings.Trigger, msg, re.IGNORECASE):
                args = msg.split(" ")
                self.ignoredUsers.append(args[1])
                return

            for pluginDict in self.commands:
                if re.search('^%s'+pluginDict['regex'] % Settings.Trigger, msg, re.IGNORECASE):
                    handler = pluginDict['handler']
                    args = msg.split(" ")
                    handler(nick, args)

            for pluginDict in self.triggers:
                if re.search('^'+pluginDict['regex'], msg, re.IGNORECASE):
                    handler = pluginDict['handler']
                    handler(nick, msg)

            for spam in self.spamMessages:
                if re.search(spam, msg, re.IGNORECASE):
                    time.sleep(1)
                    self.sendMessage(".timeout " + nick + "\n")
                    print("Timed out " + nick + " for spam: " + spam + ". Message was: " + msg)

        elif ircMessage.find('PING ') != -1:
            self.ircSock.send(str("PING :pong\n").encode('UTF-8'))

        elif ircMessage.find('JOIN ') != -1:
            nick = ircMessage.split('!')[0][1:]
            print(nick +" joined chat")
            for handler in self.joinPartHandlers:
                handler(nick, True)

        elif ircMessage.find('PART ') != -1:
            nick = ircMessage.split('!')[0][1:]
            print(nick +" left chat")
            for handler in self.joinPartHandlers:
                handler(nick, False)

        elif ircMessage.find('MODE '+ self.ircChan +' +o') != -1:
            nick = ircMessage.split(' ')[-1]
            if nick.lower() != Settings.Twitch_Username.lower():
                print("Mod joined: "+nick)
                for handler in self.modHandlers:
                    handler(nick, True)

        elif ircMessage.find('MODE '+ self.ircChan +' -o') != -1:
            nick = ircMessage.split(' ')[-1]
            if nick.lower() != Settings.Twitch_Username.lower():
                print("Mod left: "+nick)
                for handler in self.modHandlers:
                    handler(nick, False)

        else:
            print(ircMessage)

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

if __name__ == "__main__":
    while True:
        twitchBot = TwitchBot()
        try:
            twitchBot.loadPlugins()
            twitchBot.connect(6667)
            twitchBot.run()
        except Exception as e:
            print(traceback.format_exc(), e.message)
        twitchBot.kill()
        time.sleep(5)
