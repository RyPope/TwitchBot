__author__ = 'Ryan'
from database.SQLHelper import SQLHelper
from database.BaseQueryHelper import BaseQueryHelper
from contextlib import closing
import traceback

class LoggingQueryHelper():
    def __init__(self):
        self.queryHelper = BaseQueryHelper()
        self.sqlHelper = SQLHelper()
        self.initTables()

    def initTables(self):
        try:
            db = self.sqlHelper.getConnection()
            with closing(db.cursor()) as cur:
                cur.execute("CREATE TABLE IF NOT EXISTS `logs` "
                    "(`message_id` int NOT NULL AUTO_INCREMENT,"
                    "`channel_id` int NOT NULL,"
                    "`user_id` int NOT NULL,"
                    "`msg` text,"
                    "`timestamp` datetime DEFAULT CURRENT_TIMESTAMP,"
                    "PRIMARY KEY (`message_id`))")
                db.commit()

        except Exception as e:
            print("Error initializing logging tables")
            print(traceback.format_exc())
        finally:
            db.close()

    def insertMsg(self, username, channel, msg):
        try:
            db = self.sqlHelper.getConnection()
            with closing(db.cursor()) as cur:
                channel_id = self.queryHelper.getChannelID(channel)
                user_id = self.queryHelper.getUserID(username)

                cur.execute("""INSERT IGNORE INTO `logs` (`channel_id`, `user_id`, `msg`) VALUES(%s, %s, %s)""", (channel_id, user_id, msg))
                db.commit()

        except Exception as e:
            print("Error inserting new msg")
            print(traceback.format_exc())
        finally:
            db.close()

    def insertUser(self, username):
        return self.queryHelper.insertUser(username)