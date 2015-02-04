__author__ = 'Ryan'
import MySQLdb
from util.BaseSettings import Settings

class SQLHelper:
    def getConnection(self):
        db = MySQLdb.connect(host=Settings.db_host, user=Settings.db_user, passwd=Settings.db_password, db=Settings.db_name)
        return db