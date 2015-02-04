__author__ = 'Ryan'

class Plugin():
    def __init__(self, plugin_row):
        self.name = plugin_row[0]
        self.channel = plugin_row[1]
        self.enabled = int(plugin_row[2])
        self.location = plugin_row[3]
