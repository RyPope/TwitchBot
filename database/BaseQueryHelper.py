__author__ = 'Ryan'
from SQLHelper import SQLHelper
from contextlib import closing
import traceback
from objects.channel import Channel

class BaseQueryHelper():
    def __init__(self):
        self.sqlHelper = SQLHelper()

    def getAllChannels(self):
        channels = []
        try:
            db = self.sqlHelper.getConnection()

            with closing(db.cursor()) as cur:
                cur.execute("SELECT * FROM channels")
                rows = cur.fetchall()

                for row in rows:
                    channels.append(Channel(row))

        except Exception as e:
            print(traceback.format_exc())
        finally:
            db.close()
            return channels


    def checkPluginDisabled(self, channel, plugin):
        disabled = False
        try:
            db = self.sqlHelper.getConnection()

            with closing(db.cursor()) as cur:
                cur.execute("""SELECT plugin FROM disabled_plugins WHERE plugin = %s AND channel = %s""", (plugin, channel))

                result = cur.fetchone()
                if not result == None:
                    disabled = True

        except Exception as e:
            print(traceback.format_exc())
        finally:
            db.close()
            return disabled

    def channelIsEnabled(self, channel):
        enabled = False
        try:
            db = self.sqlHelper.getConnection()

            with closing(db.cursor()) as cur:
                channel_id = self.getChannelID(channel)
                cur.execute("""SELECT enabled FROM channels WHERE channel_id = %s""", (channel_id,))

                result = cur.fetchone()
                if result == None:
                    enabled = False
                elif result[0] == 1:
                    enabled = True

        except Exception as e:
            print(traceback.format_exc())
        finally:
            db.close()
            return enabled

    def isAdmin(self, user):
        admin = False
        try:
            db = self.sqlHelper.getConnection()

            with closing(db.cursor()) as cur:
                cur.execute("""SELECT is_admin FROM users WHERE username = %s""", (user,))

                result = cur.fetchone()[0]
                if not result == None:
                    admin = int(result) == 1

        except Exception as e:
            print(traceback.format_exc())
        finally:
            db.close()
            return admin

    def addChannel(self, channel, moderator, enabled=True):
        try:
            db = self.sqlHelper.getConnection()
            with closing(db.cursor()) as cur:
                enabled_int = 1 if enabled else 0
                cur.execute("""INSERT IGNORE INTO channels (channel, enabled) VALUES(%s, %s)""", (channel, enabled_int))
                db.commit()

                channel_id = self.getChannelID(channel)
                user_id = self.getUserID(moderator)

                cur.execute("""INSERT IGNORE INTO mods (channel_id, user_id) VALUES(%s, %s)""", (channel_id, user_id))
                db.commit()

        except Exception as e:
            print("Error inserting new channel")
            print(traceback.format_exc())
        finally:
            db.close()

    def removeChannel(self, channel):
        try:
            db = self.sqlHelper.getConnection()
            with closing(db.cursor()) as cur:
                channel_id = self.getChannelID(channel)
                cur.execute("""DELETE FROM channels WHERE channel_id = %s""", (channel_id,))
                cur.execute("""DELETE FROM mods WHERE channel_id = %s""", (channel_id,))
                db.commit()

        except Exception as e:
            print("Error inserting new channel")
            print(traceback.format_exc())
        finally:
            db.close()

    def getChannelID(self, channel):
        channel_id = None
        try:
            db = self.sqlHelper.getConnection()

            with closing(db.cursor()) as cur:
                cur.execute("""SELECT channel_id FROM channels WHERE channel = %s""", (channel,))

                result = cur.fetchone()[0]
                if not result == None:
                    channel_id = result

        except Exception as e:
            print("Error fetching channel ID")
            print(traceback.format_exc())
        finally:
            db.close()
            return channel_id

    def getUserID(self, username):
        user_id = None
        try:
            db = self.sqlHelper.getConnection()

            with closing(db.cursor()) as cur:
                self.insertUser(username)
                cur.execute("""SELECT user_id FROM users WHERE username = %s""", (username,))

                result = cur.fetchone()[0]
                if not result == None:
                    user_id = result

        except Exception as e:
            print("Error fetching user ID")
            print(traceback.format_exc())
        finally:
            db.close()
            return user_id

    def insertUser(self, username):
        try:
            db = self.sqlHelper.getConnection()
            with closing(db.cursor()) as cur:
                cur.execute("""INSERT IGNORE INTO users
                (username)
                VALUES(%s)""", (username,))
                db.commit()

        except Exception as e:
            print("Error inserting new user")
            print(traceback.format_exc())
        finally:
            db.close()

    def isMod(self, username, channel):
        mod = False
        try:
            db = self.sqlHelper.getConnection()

            with closing(db.cursor()) as cur:
                user_id = self.getUserID(username)
                channel_id = self.getChannelID(channel)

                cur.execute("""SELECT COUNT(*) FROM mods
                WHERE user_id = %s
                AND channel_id = %s""", (user_id, channel_id))

                result = cur.fetchone()
                if not result is None:
                    mod = int(result[0]) == 1

        except Exception as e:
            print(traceback.format_exc())
        finally:
            db.close()
            return mod

    def getUsername(self, user_id):
        username = ""
        try:
            db = self.sqlHelper.getConnection()

            with closing(db.cursor()) as cur:
                cur.execute("""SELECT username FROM users WHERE user_id = %s""", (user_id,))

                result = cur.fetchone()
                if not result is None:
                    username = str(result[0])

        except Exception as e:
            print(traceback.format_exc())
        finally:
            db.close()
            return username

    def setSetting(self, channel, key, value):
        try:
            db = self.sqlHelper.getConnection()
            with closing(db.cursor()) as cur:
                channel_id = self.getChannelID(channel)

                cur.execute("""INSERT INTO `settings` (`channel_id`, `key`, `value`)
                VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE `value` = %s;""", (channel_id, key, value, value))
                db.commit()

        except Exception as e:
            print("Error inserting new setting")
            print(traceback.format_exc())
        finally:
            db.close()