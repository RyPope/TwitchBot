__author__ = 'Ryan'

class Advertisement():
    def __init__(self, ad_row):
        self.channel_id = int(ad_row[0])
        self.interval = int(ad_row[1])
        self.message = ad_row[2]