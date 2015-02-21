__author__ = 'Ryan'
from database.SQLHelper import SQLHelper
from database.BaseQueryHelper import BaseQueryHelper
from plugins.LoggingPlugin.LoggingQueryHelper import LoggingQueryHelper
from contextlib import closing
import traceback


class GameQueryHelper():
    def __init__(self):
        self.queryHelper = BaseQueryHelper()
        self.loggingQueryHelper = LoggingQueryHelper()
        self.sqlHelper = SQLHelper()

    def isMod(self, username, channel):
        return self.queryHelper.isMod(username, channel)

    def isAdmin(self, username):
        return self.queryHelper.isAdmin(username)

    def getPoints(self, username, channel):
        return self.loggingQueryHelper.getPoints(username, channel)