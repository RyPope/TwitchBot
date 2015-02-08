__author__ = 'Ryan'
from database.SQLHelper import SQLHelper
from database.BaseQueryHelper import BaseQueryHelper
from contextlib import closing
import traceback


class AdminQueryHelper():
    def __init__(self):
        self.queryHelper = BaseQueryHelper()
        self.sqlHelper = SQLHelper()

    def isMod(self, username, channel):
        mod = False
        try:
            db = self.sqlHelper.getConnection()

            with closing(db.cursor()) as cur:
                user_id = self.queryHelper.getUserID(username)
                channel_id = self.queryHelper.getChannelID(channel)

                cur.execute("""SELECT COUNT(*) FROM mods
                WHERE user_id = %s
                AND channel_id = %s""", (user_id, channel_id))

                result = cur.fetchone()
                if not result == None:
                    mod = int(result[0]) == 1

        except Exception as e:
            print(traceback.format_exc())
        finally:
            db.close()
            return mod

    def isAdmin(self, username):
        return self.queryHelper.isAdmin(username)

    def addChannel(self, channel, moderator):
        return self.queryHelper.addChannel(channel, moderator)

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