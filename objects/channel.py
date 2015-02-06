__author__ = 'Ryan'

class Channel():
    def __init__(self, channel_row):
        self.channel_id = int(channel_row[0])
        self.channel = channel_row[1]
        self.enabled = int(channel_row[2])
