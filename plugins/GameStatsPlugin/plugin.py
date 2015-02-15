from plugins.BasePlugin import BasePlugin
from plugins.GameStatsPlugin import GameStatsQueryHelper
from bs4 import BeautifulSoup
import urllib2
import traceback
import time
from twisted.internet.task import LoopingCall

class GameStatsPlugin(BasePlugin):
    def __init__(self, twitchBot):
        super(GameStatsPlugin, self).__init__(twitchBot)
        self.className = self.__class__.__name__

        self.updateLoop = LoopingCall(self.updateMatches)
        self.updateLoop.start(120)

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

        for game in gamesToUpdate:
            try:
                link = ""
                if game == "csgo":
                    link = csgoMatchLink
                elif game == "lol":
                    link = lolMatchLink
                elif game == "dota2":
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
                            opponent1 = match_info.find("span", attrs={ "class" : "opp1" } ).text.strip()
                            bet1 = match_info.find("span", attrs={ "class" : "bet1" } ).text.strip()
                            opponent2 = match_info.find("span", attrs={ "class" : "opp2" } ).text.strip()
                            bet2 = match_info.find("span", attrs={ "class" : "bet2" } ).text.strip()

                            # Add game to list
                            print("%s - %s: %s %s vs %s %s" % (game, header, opponent1, bet1, opponent2, bet2))


            except Exception as e:
                print("Error retrieving game data")
                print(traceback.format_exc())
