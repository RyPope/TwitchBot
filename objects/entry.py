__author__ = 'Ryan'

class Entry:
    def __init__(self, username, channel, points):
        self.username = username.encode("UTF-8")
        self.channel = channel.encode("UTF-8")
        self.points = points