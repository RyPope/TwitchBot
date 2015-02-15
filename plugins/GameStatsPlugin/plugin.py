from plugins.BasePlugin import BasePlugin
from plugins.GameStatsPlugin import GameStatsQueryHelper
from bs4 import BeautifulSoup
import urllib2
import traceback
import time
from twisted.internet.task import LoopingCall
from objects.game import Game

class GameStatsPlugin(BasePlugin):
    def __init__(self, twitchBot):
        super(GameStatsPlugin, self).__init__(twitchBot)
        self.className = self.__class__.__name__

        self.updateLoop = LoopingCall(self.updateMatches)
        self.updateLoop.start(120)

        self.registerCommand(self.className, "live", self.liveListHandler)
        self.registerCommand(self.className, "upcoming", self.upcomingListHandler)

    def liveListHandler(self, user, chan, args):
        if len(args) < 2:
            self.sendMessage(self.className, chan, "Invalid syntax, please use live <csgo | dota2 | lol>")
        else:
            if args[1] == "csgo":
                if len(self.csgoLiveList) == 0:
                    self.sendMessage(self.className, chan, "No matches are scheduled for Counter Strike: Global Offensive")
                for game in self.csgoLiveList:
                    self.sendMessage(self.className, chan, "ID: %s - %s %s vs %s %s"
                                     % (game.id, game.opp1, game.bet1, game.opp2, game.bet2))
            elif args[1] == "dota2":
                if len(self.dotaLiveList) == 0:
                    self.sendMessage(self.className, chan, "No matches are scheduled for Dota 2")
                for game in self.dotaLiveList:
                    self.sendMessage(self.className, chan, "ID: %s - %s %s vs %s %s"
                                     % (game.id, game.opp1, game.bet1, game.opp2, game.bet2))
            elif args[1] == "lol":
                if len(self.lolLiveList) == 0:
                    self.sendMessage(self.className, chan, "No matches are scheduled for League of Legends")
                for game in self.lolLiveList:
                    self.sendMessage(self.className, chan, "ID: %s - %s %s vs %s %s"
                                     % (game.id, game.opp1, game.bet1, game.opp2, game.bet2))
            else:
                self.sendMessage(self.className, chan, "Invalid game type, select either csgo, dota2 or lol")

    def upcomingListHandler(self, user, chan, args):
        if len(args) < 2:
            self.sendMessage(self.className, chan, "Invalid syntax, please use upcoming <csgo | dota2 | lol>")
        else:
            if args[1] == "csgo":
                if len(self.csgoUpcomingList) == 0:
                    self.sendMessage(self.className, chan, "No matches are currently live for Counter Strike: Global Offensive")
                for game in self.csgoUpcomingList:
                    self.sendMessage(self.className, chan, "ID: %s - %s %s vs %s %s. Time To Match: %s"
                                     % (game.id, game.opp1, game.bet1, game.opp2, game.bet2, game.timeUntil))
            elif args[1] == "dota2":
                if len(self.dotaUpcomingList) == 0:
                    self.sendMessage(self.className, chan, "No matches are currently live for Dota 2")
                for game in self.dotaUpcomingList:
                    self.sendMessage(self.className, chan, "ID: %s - %s %s vs %s %s. Time To Match: %s"
                                     % (game.id, game.opp1, game.bet1, game.opp2, game.bet2, game.timeUntil))
            elif args[1] == "lol":
                if len(self.lolUpcomingList) == 0:
                    self.sendMessage(self.className, chan, "No matches are currently live for League of Legends")
                for game in self.lolUpcomingList:
                    self.sendMessage(self.className, chan, "ID: %s - %s %s vs %s %s. Time To Match: %s"
                                     % (game.id, game.opp1, game.bet1, game.opp2, game.bet2, game.timeUntil))
            else:
                self.sendMessage(self.className, chan, "Invalid game type, select either csgo, dota2 or lol")

    def clearLists(self):
        self.csgoUpcomingList = []
        self.csgoLiveList = []
        self.csgoRecentList = []

        self.dotaUpcomingList = []
        self.dotaLiveList = []
        self.dotaRecentList = []

        self.lolUpcomingList = []
        self.lolLiveList = []
        self.lolRecentList = []

    def updateMatches(self):
        gamesToUpdate = ["csgo", "lol", "dota2"]
        csgoMatchLink = "http://www.gosugamers.net/counterstrike/gosubet"
        dotaMatchLink = "http://www.gosugamers.net/dota2/gosubet"
        lolMatchLink = "http://www.gosugamers.net/lol/gosubet"

        self.clearLists()

        for gameType in gamesToUpdate:
            try:
                link = ""
                if gameType == "csgo":
                    link = csgoMatchLink
                elif gameType == "lol":
                    link = lolMatchLink
                elif gameType == "dota2":
                    link = dotaMatchLink

                req = urllib2.Request(link, headers={'User-Agent' : "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"})
                web_page = urllib2.urlopen(req).read()
                bs = BeautifulSoup(web_page)

                match_columns = bs.findAll("div", attrs={ "id" : "col1" } )
                boxes = match_columns[0].findAll("div", attrs={ "class" : "box" } )
                for box in boxes:
                    header = ""

                    h1 = box.find("h1")
                    if h1 is None:
                        h2 = box.find("h2")
                        header = h2.text.strip()
                    else:
                        header = h1.text.strip()

                    if header.find("Live") != -1:
                        header = "Live"
                    elif header.find("Recent") != -1:
                        header = "Recent"
                    elif header.find("Upcoming") != -1:
                        header = "Upcoming"

                    table = box.find("table", attrs={ "class" : "simple" } )

                    if not table is None:
                        matches = table.find("tbody")

                        rows = matches.findAll("tr")
                        for row in rows:
                            cols = row.findAll("td")
                            match_info = cols[0].find("a", attrs={ "class" : "match" } )
                            id = match_info['href'].split("/")[-1].split("-")[0]
                            opponent1 = match_info.find("span", attrs={ "class" : "opp1" } ).text.strip()
                            bet1 = match_info.find("span", attrs={ "class" : "bet1" } ).text.strip()
                            opponent2 = match_info.find("span", attrs={ "class" : "opp2" } ).text.strip()
                            bet2 = match_info.find("span", attrs={ "class" : "bet2" } ).text.strip()

                            # Add game to list
                            game = Game(id, header, opponent1, opponent2, bet1, bet2)

                            if header == "Upcoming":
                                timeCol = cols[1].find("span", attrs={ "class" : "live-in" } )
                                timeUntil = timeCol.text.strip()
                                game.setTime(timeUntil)

                            if gameType == "csgo":
                                if header == "Live":
                                    self.csgoLiveList.append(game)
                                elif header == "Upcoming":
                                    self.csgoUpcomingList.append(game)
                                elif header == "Recent":
                                    self.csgoRecentList.append(game)
                                else:
                                    raise Exception("Parsed invalid header")
                            elif gameType == "lol":
                                if header == "Live":
                                    self.lolLiveList.append(game)
                                elif header == "Upcoming":
                                    self.lolUpcomingList.append(game)
                                elif header == "Recent":
                                    self.lolRecentList.append(game)
                                else:
                                    raise Exception("Parsed invalid header")
                            elif gameType == "dota2":
                                if header == "Live":
                                    self.dotaLiveList.append(game)
                                elif header == "Upcoming":
                                    self.dotaUpcomingList.append(game)
                                elif header == "Recent":
                                    self.dotaRecentList.append(game)
                                else:
                                    raise Exception("Parsed invalid header")

            except Exception as e:
                print("Error retrieving game data")
                print(traceback.format_exc())
