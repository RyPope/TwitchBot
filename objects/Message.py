__author__ = 'Ryan'

class Message():
    def __init__(self, message_row):
        self.message_id = int(message_row[0])
        self.channel_id = int(message_row[1])
        self.user_id = int(message_row[2])
        self.message = message_row[3]
        self.timestamp = message_row[4]