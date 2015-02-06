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

    def isAdmin(self, user):
        admin = False
        try:
            db = self.sqlHelper.getConnection()

            with closing(db.cursor()) as cur:
                cur.execute("""SELECT user FROM admins WHERE username = %s""", (user,))

                result = cur.fetchone()
                if not result == None:
                    admin = True

        except Exception as e:
            print(traceback.format_exc())
        finally:
            db.close()
            return admin