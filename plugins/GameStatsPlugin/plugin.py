from plugins.BasePlugin import BasePlugin
from plugins.GameStatsPlugin import GameStatsQueryHelper
from bs4 import BeautifulSoup
import urllib2
import traceback
import time

class GameStatsPlugin(BasePlugin):
    def __init__(self, twitchBot):
        super(GameStatsPlugin, self).__init__(twitchBot)
        self.className = self.__class__.__name__
        # self.queryHelper = GameStatsQueryHelper()

        self.registerCommand(self.className, "updatematches", self.updateMatchesHandler)

    def updateMatchesHandler(self, username, channel, args):
        if len(args) < 2:
            self.sendMessage(self.className, channel, "Invalid Syntax, use updatematches <game>")
        else:
            self.getMatchList(args[1], channel)

    def getMatchList(self, game, channel):
        csgoMatchLink = "http://www.gosugamers.net/counterstrike/gosubet"
        if game == "csgo":
            try:
                req = urllib2.Request(csgoMatchLink, headers={'User-Agent' : "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"})
                web_page = urllib2.urlopen(req).read()
                bs = BeautifulSoup(web_page)
                table = bs.findAll("table", attrs={ "class" : "simple" } )
                upcoming_matches = table[0].find("tbody")

                rows = upcoming_matches.findAll("tr")
                for row in rows:
                    cols = row.findAll("td")
                    match_info = cols[0].find("a", attrs={ "class" : "match" } )
                    opponent1 = match_info.find("span", attrs={ "class" : "opp1" } ).text.strip()
                    bet1 = match_info.find("span", attrs={ "class" : "bet1" } ).text.strip()
                    opponent2 = match_info.find("span", attrs={ "class" : "opp2" } ).text.strip()
                    bet2 = match_info.find("span", attrs={ "class" : "bet2" } ).text.strip()

                    self.sendMessage(self.className, channel, "Upcoming: %s %s vs %s %s" % (opponent1, bet1, opponent2, bet2))
                    time.sleep(.25)


            except Exception as e:
                print("Error retrieving game page")
                print(traceback.format_exc())
