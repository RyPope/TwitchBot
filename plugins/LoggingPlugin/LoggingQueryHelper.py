__author__ = 'Ryan'
from database.SQLHelper import SQLHelper
from database.BaseQueryHelper import BaseQueryHelper
from contextlib import closing
import traceback
from objects.message import Message
import datetime

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

                cur.execute("CREATE TABLE IF NOT EXISTS `time_spent`"
                            "(`user_id` int NOT NULL,"
                            "`channel_id` int NOT NULL,"
                            "`time_spent` int NOT NULL DEFAULT 0,"
                            "`points` double NOT NULL DEFAULT 0,"
                            "PRIMARY KEY (`user_id`, `channel_id`))")
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

    def getMessages(self, username, channel):
        messages = []
        try:
            db = self.sqlHelper.getConnection()

            with closing(db.cursor()) as cur:
                channel_id = self.queryHelper.getChannelID(channel)
                user_id = self.queryHelper.getUserID(username)

                cur.execute("""SELECT * FROM `logs` WHERE `channel_id` = %s AND `user_id` = %s""", (channel_id, user_id))
                rows = cur.fetchall()

                for row in rows:
                    messages.append(Message(row))

        except Exception as e:
            print(traceback.format_exc())
        finally:
            db.close()
            return messages

    def updateTimeSpent(self, username, channel, time):
        try:
            db = self.sqlHelper.getConnection()
            with closing(db.cursor()) as cur:
                channel_id = self.queryHelper.getChannelID(channel)
                user_id = self.queryHelper.getUserID(username)

                cur.execute("""INSERT INTO `time_spent` (`channel_id`, `user_id`) VALUES (%s, %s) ON DUPLICATE KEY
                UPDATE `time_spent` = `time_spent` + %s, `points` = `points` + %s""", (channel_id, user_id, time, time))

                db.commit()

        except Exception as e:
            print("Error inserting new time spent")
            print(traceback.format_exc())
        finally:
            db.close()

    def deductPoints(self, username, channel, points):
        try:
            db = self.sqlHelper.getConnection()
            with closing(db.cursor()) as cur:
                channel_id = self.queryHelper.getChannelID(channel)
                user_id = self.queryHelper.getUserID(username)

                cur.execute("""INSERT INTO `time_spent` (`channel_id`, `user_id`) VALUES (%s, %s) ON DUPLICATE KEY
                UPDATE `points` = `points` - %s""", (channel_id, user_id, points))

                db.commit()

        except Exception as e:
            print("Error deducting points")
            print(traceback.format_exc())
        finally:
            db.close()

    def increasePoints(self, username, channel, points):
        try:
            db = self.sqlHelper.getConnection()
            with closing(db.cursor()) as cur:
                channel_id = self.queryHelper.getChannelID(channel)
                user_id = self.queryHelper.getUserID(username)

                cur.execute("""INSERT INTO `time_spent` (`channel_id`, `user_id`) VALUES (%s, %s) ON DUPLICATE KEY
                UPDATE `points` = `points` + %s""", (channel_id, user_id, points))

                db.commit()

        except Exception as e:
            print("Error awarding points")
            print(traceback.format_exc())
        finally:
            db.close()

    def getPoints(self, username, channel):
        value = None
        try:
            db = self.sqlHelper.getConnection()

            with closing(db.cursor()) as cur:
                channel_id = self.queryHelper.getChannelID(channel)
                user_id = self.queryHelper.getUserID(username)

                cur.execute("""SELECT `points` FROM `time_spent` WHERE `channel_id` = %s AND `user_id` = %s""", (channel_id, user_id))

                result = cur.fetchone()
                if not result is None:
                    value = result[0]

        except Exception as e:
            print(traceback.format_exc())
        finally:
            db.close()
            return value