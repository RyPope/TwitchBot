__author__ = 'Ryan'
from database.SQLHelper import SQLHelper
from database.BaseQueryHelper import BaseQueryHelper
from contextlib import closing
import traceback


class AdminQueryHelper():
    def __init__(self):
        self.queryHelper = BaseQueryHelper()
        self.sqlHelper = SQLHelper()
        self.initTables()

    def initTables(self):
        try:
            db = self.sqlHelper.getConnection()
            with closing(db.cursor()) as cur:
                cur.execute("CREATE TABLE IF NOT EXISTS `bug_log` "
                            "(`bug_id` int NOT NULL AUTO_INCREMENT,"
                            "`user_id` int,"
                            "`channel_id` int,"
                            "`description` TEXT,"
                            "PRIMARY KEY (`bug_id`))")

                cur.execute("CREATE TABLE IF NOT EXISTS `mail_log` "
                            "(`mail_id` int NOT NULL AUTO_INCREMENT,"
                            "`user_id` int,"
                            "`channel_id` int,"
                            "`message` TEXT,"
                            "PRIMARY KEY (`mail_id`))")
                db.commit()

        except Exception as e:
            print("Error initializing admin tables")
            print(traceback.format_exc())
        finally:
            db.close()

    def isMod(self, username, channel):
        return self.queryHelper.isMod(username, channel)

    def isAdmin(self, username):
        return self.queryHelper.isAdmin(username)

    def addChannel(self, channel, moderator, enabled=True):
        return self.queryHelper.addChannel(channel, moderator, enabled)

    def removeChannel(self, channel):
        return self.queryHelper.removeChannel(channel)

    def addMod(self, username, channel):
        try:
            db = self.sqlHelper.getConnection()
            with closing(db.cursor()) as cur:
                user_id = self.queryHelper.getUserID(username)
                channel_id = self.queryHelper.getChannelID(channel)

                cur.execute("""INSERT IGNORE INTO mods (channel_id, user_id) VALUES(%s, %s)""", (channel_id, user_id))
                db.commit()

        except Exception as e:
            print("Error inserting new moderator")
            print(traceback.format_exc())
        finally:
            db.close()

    def logBug(self, username, channel, description):
        try:
            db = self.sqlHelper.getConnection()
            with closing(db.cursor()) as cur:
                user_id = self.queryHelper.getUserID(username)
                channel_id = self.queryHelper.getChannelID(channel)

                cur.execute("""INSERT IGNORE INTO `bug_log` (`channel_id`, `user_id`, `description`) VALUES(%s, %s, %s)""", (channel_id, user_id, description))
                db.commit()

        except Exception as e:
            print("Error inserting new bug")
            print(traceback.format_exc())
        finally:
            db.close()

    def logMail(self, username, channel, message):
        try:
            db = self.sqlHelper.getConnection()
            with closing(db.cursor()) as cur:
                user_id = self.queryHelper.getUserID(username)
                channel_id = self.queryHelper.getChannelID(channel)

                cur.execute("""INSERT IGNORE INTO `mail_log` (`channel_id`, `user_id`, `message`) VALUES(%s, %s, %s)""", (channel_id, user_id, message))
                db.commit()

        except Exception as e:
            print("Error inserting mail")
            print(traceback.format_exc())
        finally:
            db.close()

    def removeMod(self, username, channel):
        try:
            db = self.sqlHelper.getConnection()
            with closing(db.cursor()) as cur:
                user_id = self.queryHelper.getUserID(username)
                channel_id = self.queryHelper.getChannelID(channel)

                cur.execute("""DELETE FROM mods WHERE user_id = %s AND channel_id = %s""", (user_id, channel_id))
                db.commit()

        except Exception as e:
            print("Error removing moderator")
            print(traceback.format_exc())
        finally:
            db.close()

    def viewMods(self, channel):
        mods = []
        try:
            db = self.sqlHelper.getConnection()

            with closing(db.cursor()) as cur:
                channel_id = self.queryHelper.getChannelID(channel)

                cur.execute("""SELECT user_id FROM mods WHERE channel_id = %s""", (channel_id,))
                rows = cur.fetchall()

                for row in rows:
                    mods.append(self.queryHelper.getUsername(row[0]))

        except Exception as e:
            print(traceback.format_exc())
        finally:
            db.close()
            return mods

    def addCommand(self, channel, trigger, output):
        try:
            db = self.sqlHelper.getConnection()
            with closing(db.cursor()) as cur:
                channel_id = self.queryHelper.getChannelID(channel)

                cur.execute("""INSERT INTO `commands` (`channel_id`, `key`, `value`)
                VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE `value` = %s;""", (channel_id, trigger, output, output))
                db.commit()

        except Exception as e:
            print("Error inserting new command")
            print(traceback.format_exc())
        finally:
            db.close()

    def removeCommand(self, channel, key):
        try:
            db = self.sqlHelper.getConnection()
            with closing(db.cursor()) as cur:
                channel_id = self.queryHelper.getChannelID(channel)

                cur.execute("""DELETE FROM `commands` WHERE `channel_id` = %s AND `key` = %s""", (channel_id, key))
                db.commit()

        except Exception as e:
            print("Error removing command")
            print(traceback.format_exc())
        finally:
            db.close()

    def viewCommands(self, channel):
        commands = []
        try:
            db = self.sqlHelper.getConnection()

            with closing(db.cursor()) as cur:
                channel_id = self.queryHelper.getChannelID(channel)

                cur.execute("""SELECT `key` FROM `commands` WHERE `channel_id` = %s""", (channel_id,))
                rows = cur.fetchall()

                for row in rows:
                    commands.append(str(row[0]))

        except Exception as e:
            print(traceback.format_exc())
        finally:
            db.close()
            return commands

    def getCommand(self, channel, key):
        value = None
        try:
            db = self.sqlHelper.getConnection()

            with closing(db.cursor()) as cur:
                channel_id = self.queryHelper.getChannelID(channel)

                cur.execute("""SELECT `value` FROM `commands` WHERE `channel_id` = %s AND `key` = %s""", (channel_id, key))

                result = cur.fetchone()
                if not result is None:
                    value = str(result[0])

        except Exception as e:
            print(traceback.format_exc())
        finally:
            db.close()
            return value