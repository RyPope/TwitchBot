__author__ = 'Ryan'
from database.SQLHelper import SQLHelper
from database.BaseQueryHelper import BaseQueryHelper
from contextlib import closing
import traceback
from objects.advertisement import Advertisement

class AdQueryHelper():
    def __init__(self):
        self.queryHelper = BaseQueryHelper()
        self.sqlHelper = SQLHelper()

        self.initTables()

    def initTables(self):
        try:
            db = self.sqlHelper.getConnection()
            with closing(db.cursor()) as cur:
                cur.execute("CREATE TABLE IF NOT EXISTS `advertisements` "
                            "(`channel_id` int NOT NULL AUTO_INCREMENT,"
                            "`time` int DEFAULT 5,"
                            "`message` TEXT,"
                            "`enabled` tinyint(1) DEFAULT 1,"
                            "PRIMARY KEY (`channel_id`))")

                db.commit()

        except Exception as e:
            print("Error initializing advertisement tables")
            print(traceback.format_exc())
        finally:
            db.close()

    def isMod(self, username, channel):
        return self.queryHelper.isMod(username, channel)

    def isAdmin(self, username):
        return self.queryHelper.isAdmin(username)

    def insertOrUpdateAd(self, channel, interval, message):
        try:
            db = self.sqlHelper.getConnection()
            with closing(db.cursor()) as cur:
                channel_id = self.queryHelper.getChannelID(channel)

                cur.execute("""INSERT INTO `advertisements` (`channel_id`, `time`, `message`)
                VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE `time` = %s, `message` = %s;""",
                            (channel_id, interval, message, interval, message))
                db.commit()

        except Exception as e:
            print("Error inserting or updating advertisement")
            print(traceback.format_exc())
        finally:
            db.close()

    def getAllAds(self):
        ads = []
        try:
            db = self.sqlHelper.getConnection()

            with closing(db.cursor()) as cur:
                cur.execute("""SELECT * FROM `advertisements` WHERE `enabled` = 1""")
                rows = cur.fetchall()

                for row in rows:
                    ads.append(Advertisement(row))

        except Exception as e:
            print(traceback.format_exc())
        finally:
            db.close()
            return ads

    def getChannel(self, channel_id):
        return self.queryHelper.getChannel(channel_id)

    def setAdEnabled(self, channel, enabled):
        try:
            db = self.sqlHelper.getConnection()
            with closing(db.cursor()) as cur:
                channel_id = self.queryHelper.getChannelID(channel)
                enabled_int = 1 if enabled else 0

                cur.execute("""UPDATE `advertisements` SET `enabled` = %s WHERE `channel_id` = %s""", (enabled_int, channel_id))

                db.commit()

        except Exception as e:
            print("Error updating ad enabled")
            print(traceback.format_exc())
        finally:
            db.close()

    def getAdFromID(self, channel_id):
        ad = None
        try:
            db = self.sqlHelper.getConnection()

            with closing(db.cursor()) as cur:
                cur.execute("""SELECT * FROM `advertisements` WHERE `channel_id` = %s""", (channel_id,))
                row = cur.fetchone()

                ad = Advertisement(row)

        except Exception as e:
            print(traceback.format_exc())
        finally:
            db.close()
            return ad