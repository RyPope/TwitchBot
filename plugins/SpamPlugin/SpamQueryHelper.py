__author__ = 'Ryan'
from database.SQLHelper import SQLHelper
from database.BaseQueryHelper import BaseQueryHelper
from contextlib import closing
import traceback


class SpamQueryHelper():
    def __init__(self):
        self.queryHelper = BaseQueryHelper()
        self.sqlHelper = SQLHelper()
        self.initTables()

    def initTables(self):
        try:
            db = self.sqlHelper.getConnection()
            with closing(db.cursor()) as cur:
                cur.execute("CREATE TABLE IF NOT EXISTS `spam` "
                            "(`channel_id` int NOT NULL,"
                            "`msg` VARCHAR(256) NOT NULL,"
                            "PRIMARY KEY (channel_id, msg))")
                db.commit()

        except Exception as e:
            print("Error initializing spam tables")
            print(traceback.format_exc())
        finally:
            db.close()

    def addSpam(self, channel, msg):
        try:
            db = self.sqlHelper.getConnection()
            with closing(db.cursor()) as cur:
                channel_id = self.queryHelper.getChannelID(channel)

                cur.execute("""INSERT IGNORE INTO spam(channel_id, msg) VALUES(%s, %s)""", (channel_id, msg))
                db.commit()

        except Exception as e:
            print("Error inserting new spam message")
            print(traceback.format_exc())
        finally:
            db.close()

    def getSpam(self, channel):
        spamMessages = []
        try:
            db = self.sqlHelper.getConnection()

            with closing(db.cursor()) as cur:
                channel_id = self.queryHelper.getChannelID(channel)

                cur.execute("""SELECT msg FROM spam WHERE channel_id = %s""", (channel_id,))
                rows = cur.fetchall()

                for row in rows:
                    spamMessages.append(str(row[0]))

        except Exception as e:
            print(traceback.format_exc())
        finally:
            db.close()
            return spamMessages

    def removeSpam(self, channel, msg):
        try:
            db = self.sqlHelper.getConnection()
            with closing(db.cursor()) as cur:
                channel_id = self.queryHelper.getChannelID(channel)

                cur.execute("""DELETE FROM spam WHERE channel_id = %s AND msg = %s""", (channel_id, msg))
                db.commit()

        except Exception as e:
            print("Error removing spam")
            print(traceback.format_exc())
        finally:
            db.close()

    def isMod(self, username, channel):
        return self.queryHelper.isMod(username, channel)

    def isAdmin(self, username):
        return self.queryHelper.isAdmin(username)