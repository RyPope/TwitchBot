__author__ = 'Ryan'

class Bet():
    def __init__(self, bet_row):
        self.match_id = int(bet_row[0])
        self.channel_id = int(bet_row[1])
        self.user_id = int(bet_row[2])
        self.status = bet_row[3]
        self.match_id = bet_row[4]
        self.betFor = bet_row[5]
        self.betAmount = bet_row[6]