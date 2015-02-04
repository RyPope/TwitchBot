__author__ = 'Ryan'

class Channel():
    def __init__(self, channel_row):
        self.channel = channel_row[0]
        self.enabled = int(channel_row[1])
        self.admin = channel_row[2]
        self.startDate = channel_row[3]
        self.expiryDate = channel_row[4]
