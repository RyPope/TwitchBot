__author__ = 'Ryan'
import MySQLdb
from util.BaseSettings import Settings
import traceback
from contextlib import closing
from warnings import filterwarnings, resetwarnings

class SQLHelper:
    def __init__(self):
        filterwarnings('ignore', category = MySQLdb.Warning) # SQL warns on DB creation for whatever reason.
        self.initDB()
        self.initTables()
        resetwarnings()

    def getConnection(self):
        db = MySQLdb.connect(host=Settings.db_host, user=Settings.db_user, passwd=Settings.db_password, db=Settings.db_name)
        return db

    def initDB(self):
        try:
            db = MySQLdb.connect(host=Settings.db_host, user=Settings.db_user, passwd=Settings.db_password)
            with closing(db.cursor()) as cur:
                cur.execute("CREATE DATABASE IF NOT EXISTS %s" % Settings.db_name)

                db.commit()

        except Exception as e:
            print("Error initializing DB")
            print(traceback.format_exc())
        finally:
            db.close()

    def initTables(self):
        try:
            db = self.getConnection()
            with closing(db.cursor()) as cur:
                cur.execute("CREATE TABLE IF NOT EXISTS `channels` "
                            "(`channel` text NOT NULL,"
                            "`enabled` tinyint(1) NOT NULL,"
                            "`admin` text NOT NULL,"
                            "`sub_start` datetime NOT NULL,"
                            "`sub_end` datetime NOT NULL)")

                cur.execute("CREATE TABLE IF NOT EXISTS `ignored_users` "
                            "(`channel` text NOT NULL,"
                            "`admin` text NOT NULL,"
                            "`user` text NOT NULL,"
                            "`created_on` datetime NOT NULL,"
                            "`expires_on` datetime NOT NULL)")

                cur.execute("CREATE TABLE IF NOT EXISTS `plugins` "
                            "(`name` text NOT NULL,"
                            "`channel` text NOT NULL,"
                            "`enabled` tinyint(1) NOT NULL,"
                            "`location` text NOT NULL)")

                cur.execute("CREATE TABLE IF NOT EXISTS `settings` "
                            "(`channel` text NOT NULL,"
                            "`key` text NOT NULL,"
                            "`value` text NOT NULL)")

                cur.execute("CREATE TABLE IF NOT EXISTS `spam_triggers` "
                            "(`channel` text NOT NULL,"
                            "`value` text NOT NULL,"
                            "`created_on` datetime NOT NULL,"
                            "`expires_on` datetime NOT NULL)")

                db.commit()

        except Exception as e:
            print("Error initializing DB")
            print(traceback.format_exc())
        finally:
            db.close()