__author__ = 'Ryan'

class Game:
    def __init__(self, game, id, type, link, opp1, opp2, bet1, bet2):
        self.game = game
        self.id = id
        self.type = type
        self.link = link
        self.opp1 = opp1
        self.opp2 = opp2
        self.bet1 = bet1
        self.bet2 = bet2
        self.timeUntil = ""
        self.score = ""

    def setTime(self, time):
        self.timeUntil = time

    def setScore(self, score):
        self.score = score