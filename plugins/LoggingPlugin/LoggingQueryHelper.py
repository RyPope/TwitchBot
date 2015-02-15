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

                cur.execute("CREATE TABLE IF NOT EXISTS `joins` "
                            "(`user_id` int NOT NULL,"
                            "`channel_id` int NOT NULL,"
                            "`joined` datetime NOT NULL,"
                            "PRIMARY KEY (`user_id`, `channel_id`))")

                cur.execute("CREATE TABLE IF NOT EXISTS `time_spent`"
                            "(`user_id` int NOT NULL,"
                            "`channel_id` int NOT NULL,"
                            "`time_spent` int NOT NULL DEFAULT 0,"
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

    def insertJoined(self, username, channel, time):
        try:
            db = self.sqlHelper.getConnection()
            with closing(db.cursor()) as cur:
                channel_id = self.queryHelper.getChannelID(channel)
                user_id = self.queryHelper.getUserID(username)

                cur.execute("""INSERT IGNORE INTO `joins` (`channel_id`, `user_id`, `joined`) VALUES(%s, %s, %s)""", (channel_id, user_id, time))
                db.commit()

        except Exception as e:
            print("Error inserting new join")
            print(traceback.format_exc())
        finally:
            db.close()

    def popJoined(self, username, channel):
        joinTime = datetime.datetime.now()
        try:
            db = self.sqlHelper.getConnection()

            with closing(db.cursor()) as cur:
                channel_id = self.queryHelper.getChannelID(channel)
                user_id = self.queryHelper.getUserID(username)

                cur.execute("""SELECT joined FROM `joins` WHERE `channel_id` = %s AND `user_id` = %s""", (channel_id, user_id))
                joined = cur.fetchone()

                if not joined is None:
                    joinTime = joined[0]

                cur.execute("""DELETE FROM joins WHERE user_id = %s AND channel_id = %s""", (user_id, channel_id))
                db.commit()

        except Exception as e:
            print(traceback.format_exc())
        finally:
            db.close()
            return joinTime

    def updateTimeSpent(self, username, channel, time):
        try:
            db = self.sqlHelper.getConnection()
            with closing(db.cursor()) as cur:
                channel_id = self.queryHelper.getChannelID(channel)
                user_id = self.queryHelper.getUserID(username)

                cur.execute("""UPDATE `time_spent` SET `time_spent` = `time_spent` + %s WHERE `user_id` = %s AND `channel_id` = %s""", (time, user_id, channel_id))
                db.commit()

        except Exception as e:
            print("Error inserting new time spent")
            print(traceback.format_exc())
        finally:
            db.close()