__author__ = 'Ryan'
from SQLHelper import SQLHelper
from contextlib import closing
import traceback
from objects.channel import Channel

class QueryHelper():
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


    def checkPluginEnabled(self, channel, plugin):
        enabled = True
        try:
            db = self.sqlHelper.getConnection()

            with closing(db.cursor()) as cur:
                cur.execute("""SELECT enabled FROM plugins WHERE name = %s AND channel = %s""", (plugin, channel))

                result = cur.fetchone()
                if not result == None:
                    enabled = int(result[0]) == 1

        except Exception as e:
            print(traceback.format_exc())
        finally:
            db.close()
            return enabled

    def getSpamMessages(self):
        spamMessages = []
        try:
            db = self.sqlHelper.getConnection()

            with closing(db.cursor()) as cur:
                cur.execute("""SELECT message FROM spam_messages""")
                rows = cur.fetchall()

                for message in rows:
                    spamMessages.append(str(message))

        except Exception as e:
            print(traceback.format_exc())
        finally:
            db.close()
            return spamMessages

    def isAdmin(self, username):
        admin = False
        try:
            db = self.sqlHelper.getConnection()

            with closing(db.cursor()) as cur:
                cur.execute("""SELECT username FROM admins WHERE username = %s""", (username,))

                result = cur.fetchone()
                if not result == None:
                    admin = True

        except Exception as e:
            print(traceback.format_exc())
        finally:
            db.close()
            return admin

    # def addChannel(self, channel, mod):
    #     try:
    #         db = self.sqlHelper.getConnection()
    #
    #         with closing(db.cursor()) as cur:
    #             cur.execute("""INSERT username FROM admins WHERE username = %s""", (username,))
    #
    #             result = cur.fetchone()
    #             if not result == None:
    #                 admin = True
    #
    #     except Exception as e:
    #         print(traceback.format_exc())
    #     finally:
    #         db.close()