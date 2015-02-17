from plugins.BasePlugin import BasePlugin
from plugins.GameStatsPlugin.GameQueryHelper import GameQueryHelper
from bs4 import BeautifulSoup
import urllib2
import traceback
import time
import threading
from objects.game import Game

class GameStatsPlugin(BasePlugin):
    def __init__(self, twitchBot):
        super(GameStatsPlugin, self).__init__(twitchBot)
        self.className = self.__class__.__name__

        self.queryHelper = GameQueryHelper()

        self.registerCommand(self.className, "live", self.liveListHandler)
        self.registerCommand(self.className, "upcoming", self.upcomingListHandler)
        self.registerCommand(self.className, "recent", self.recentListHandler)

        self.updateMatches()

    def liveListHandler(self, user, chan, args):
        if len(args) < 2:
            self.sendMessage(self.className, chan, "Invalid syntax, please use live <csgo | dota2 | lol | hearth | hots>")
        else:
            if args[1] == "csgo":
                if len(self.csgoLiveList) == 0:
                    self.sendMessage(self.className, chan, "No matches are live for Counter Strike: Global Offensive")
                for game in self.csgoLiveList:
                    self.sendMessage(self.className, chan, "ID: %s - %s %s vs %s %s"
                                     % (game.id, game.opp1, game.bet1, game.opp2, game.bet2))
                    time.sleep(.5)

            elif args[1] == "dota2":
                if len(self.dotaLiveList) == 0:
                    self.sendMessage(self.className, chan, "No matches are live for Dota 2")
                for game in self.dotaLiveList:
                    self.sendMessage(self.className, chan, "ID: %s - %s %s vs %s %s"
                                     % (game.id, game.opp1, game.bet1, game.opp2, game.bet2))
                    time.sleep(.5)

            elif args[1] == "lol":
                if len(self.lolLiveList) == 0:
                    self.sendMessage(self.className, chan, "No matches are live for League of Legends")
                for game in self.lolLiveList:
                    self.sendMessage(self.className, chan, "ID: %s - %s %s vs %s %s"
                                     % (game.id, game.opp1, game.bet1, game.opp2, game.bet2))
                    time.sleep(.5)

            elif args[1] == "hearth":
                if len(self.hearthLiveList) == 0:
                    self.sendMessage(self.className, chan, "No matches are live for Hearthstone")
                for game in self.hearthLiveList:
                    self.sendMessage(self.className, chan, "ID: %s - %s %s vs %s %s"
                                     % (game.id, game.opp1, game.bet1, game.opp2, game.bet2))
                    time.sleep(.5)

            elif args[1] == "hots":
                if len(self.hotsLiveList) == 0:
                    self.sendMessage(self.className, chan, "No matches are live for Heroes of the Storm")
                for game in self.hotsLiveList:
                    self.sendMessage(self.className, chan, "ID: %s - %s %s vs %s %s"
                                     % (game.id, game.opp1, game.bet1, game.opp2, game.bet2))
                    time.sleep(.5)
            else:
                self.sendMessage(self.className, chan, "Invalid game type, select either csgo, dota2, hearth, hots or lol")

    def upcomingListHandler(self, user, chan, args):
        if len(args) < 2:
            self.sendMessage(self.className, chan, "Invalid syntax, please use upcoming <csgo | dota2 | lol | hearth | hots>")
        else:
            if args[1] == "csgo":
                if len(self.csgoUpcomingList) == 0:
                    self.sendMessage(self.className, chan, "No upcoming matches for Counter Strike: Global Offensive")
                for game in self.csgoUpcomingList[:5]:
                    self.sendMessage(self.className, chan, "ID: %s - %s %s vs %s %s. Time To Match: %s"
                                     % (game.id, game.opp1, game.bet1, game.opp2, game.bet2, game.timeUntil))
                    time.sleep(.5)

            elif args[1] == "dota2":
                if len(self.dotaUpcomingList) == 0:
                    self.sendMessage(self.className, chan, "No upcoming matches for Dota 2")
                for game in self.dotaUpcomingList[:5]:
                    self.sendMessage(self.className, chan, "ID: %s - %s %s vs %s %s. Time To Match: %s"
                                     % (game.id, game.opp1, game.bet1, game.opp2, game.bet2, game.timeUntil))
                    time.sleep(.5)

            elif args[1] == "lol":
                if len(self.lolUpcomingList) == 0:
                    self.sendMessage(self.className, chan, "No upcoming matches for League of Legends")
                for game in self.lolUpcomingList[:5]:
                    self.sendMessage(self.className, chan, "ID: %s - %s %s vs %s %s. Time To Match: %s"
                                     % (game.id, game.opp1, game.bet1, game.opp2, game.bet2, game.timeUntil))
                    time.sleep(.5)

            elif args[1] == "hearth":
                if len(self.hearthUpcomingList) == 0:
                    self.sendMessage(self.className, chan, "No upcoming matches for Hearthstone")
                for game in self.hearthUpcomingList[:5]:
                    self.sendMessage(self.className, chan, "ID: %s - %s %s vs %s %s. Time To Match: %s"
                                     % (game.id, game.opp1, game.bet1, game.opp2, game.bet2, game.timeUntil))
                    time.sleep(.5)

            elif args[1] == "hots":
                if len(self.hotsUpcomingList) == 0:
                    self.sendMessage(self.className, chan, "No upcoming matches for Heroes of the Storm")
                for game in self.hotsUpcomingList[:5]:
                    self.sendMessage(self.className, chan, "ID: %s - %s %s vs %s %s. Time To Match: %s"
                                     % (game.id, game.opp1, game.bet1, game.opp2, game.bet2, game.timeUntil))
                    time.sleep(.5)
            else:
                self.sendMessage(self.className, chan, "Invalid game type, select either csgo, dota2, hearth, hots or lol")

    def recentListHandler(self, user, chan, args):
        if len(args) < 2:
            self.sendMessage(self.className, chan, "Invalid syntax, please use recent <csgo | dota2 | lol | hearth | hots>")
        else:
            if args[1] == "csgo":
                if len(self.csgoRecentList) == 0:
                    self.sendMessage(self.className, chan, "No recent matches for Counter Strike: Global Offensive")
                for game in self.csgoRecentList[:5]:
                    self.sendMessage(self.className, chan, "ID: %s - %s %s vs %s %s. Score: %s"
                                     % (game.id, game.opp1, game.bet1, game.opp2, game.bet2, game.score))
                    time.sleep(.5)
            elif args[1] == "dota2":
                if len(self.dotaRecentList) == 0:
                    self.sendMessage(self.className, chan, "No recent matches for Dota 2")
                for game in self.dotaRecentList[:5]:
                    self.sendMessage(self.className, chan, "ID: %s - %s %s vs %s %s. Score: %s"
                                     % (game.id, game.opp1, game.bet1, game.opp2, game.bet2, game.score))
                    time.sleep(.5)
            elif args[1] == "lol":
                if len(self.lolRecentList) == 0:
                    self.sendMessage(self.className, chan, "No recent matches for League of Legends")
                for game in self.lolRecentList[:5]:
                    self.sendMessage(self.className, chan, "ID: %s - %s %s vs %s %s. Score: %s"
                                     % (game.id, game.opp1, game.bet1, game.opp2, game.bet2, game.score))
                    time.sleep(.5)

            elif args[1] == "hearth":
                if len(self.hearthRecentList) == 0:
                    self.sendMessage(self.className, chan, "No recent matches for Hearthstone")
                for game in self.hearthRecentList[:5]:
                    self.sendMessage(self.className, chan, "ID: %s - %s %s vs %s %s. Score: %s"
                                     % (game.id, game.opp1, game.bet1, game.opp2, game.bet2, game.score))
                    time.sleep(.5)

            elif args[1] == "hots":
                if len(self.hotsRecentList) == 0:
                    self.sendMessage(self.className, chan, "No recent matches for Heroes of the Storm")
                for game in self.hotsRecentList[:5]:
                    self.sendMessage(self.className, chan, "ID: %s - %s %s vs %s %s. Score: %s"
                                     % (game.id, game.opp1, game.bet1, game.opp2, game.bet2, game.score))
                    time.sleep(.5)
            else:
                self.sendMessage(self.className, chan, "Invalid game type, select either csgo, dota2, hearth, hots or lol")

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

        self.hearthUpcomingList = []
        self.hearthLiveList = []
        self.hearthRecentList = []

        self.hotsUpcomingList = []
        self.hotsLiveList = []
        self.hotsRecentList = []

    def updateMatches(self):
        threading.Timer(120, self.updateMatches).start()
        gamesToUpdate = ["csgo", "lol", "dota2", "hearth", "hots"]
        csgoMatchLink = "http://www.gosugamers.net/counterstrike/gosubet"
        dotaMatchLink = "http://www.gosugamers.net/dota2/gosubet"
        lolMatchLink = "http://www.gosugamers.net/lol/gosubet"
        hearthMatchLink = "http://www.gosugamers.net/hearthstone/gosubet"
        hotsMatchLink = "http://www.gosugamers.net/heroesofthestorm/gosubet"

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
                elif gameType == "hearth":
                    link = hearthMatchLink
                elif gameType == "hots":
                    link = hotsMatchLink

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
                            elif header == "Recent":
                                winnerScore = cols[1].find("span", attrs={ "class" : "hidden" } ).text.strip()
                                game.setScore(winnerScore)

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
                            elif gameType == "hearth":
                                if header == "Live":
                                    self.hearthLiveList.append(game)
                                elif header == "Upcoming":
                                    self.hearthUpcomingList.append(game)
                                elif header == "Recent":
                                    self.hearthRecentList.append(game)
                                else:
                                    raise Exception("Parsed invalid header")
                            elif gameType == "hots":
                                if header == "Live":
                                    self.hotsLiveList.append(game)
                                elif header == "Upcoming":
                                    self.hotsUpcomingList.append(game)
                                elif header == "Recent":
                                    self.hotsRecentList.append(game)
                                else:
                                    raise Exception("Parsed invalid header")

            except Exception as e:
                print("Error retrieving game data")
                print(traceback.format_exc())
