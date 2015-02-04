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
        enabled = False
        try:
            db = self.sqlHelper.getConnection()

            with closing(db.cursor()) as cur:
                cur.execute("""SELECT enabled FROM plugins WHERE name = %s AND channel = %s""", (plugin, channel))

                enabled = int(cur.fetchone()[0]) == 1

        except Exception as e:
            print(traceback.format_exc())
        finally:
            db.close()
            return enabled == True