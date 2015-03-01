__author__ = 'Ryan'
import MySQLdb
from util.BaseSettings import Settings
import traceback
from contextlib import closing
from warnings import filterwarnings, resetwarnings

class SQLHelper:
    def __init__(self):
        filterwarnings('ignore', category = MySQLdb.Warning) # SQL warns on DB creation for whatever reason.
        # self.dropDB()
        self.initDB()
        self.initTables()
        # self.insertStubData()

    def insertStubData(self):
        try:
            db = MySQLdb.connect(host=Settings.db_host, user=Settings.db_user, passwd=Settings.db_password, db=Settings.db_name)
            with closing(db.cursor()) as cur:
                cur.execute("""INSERT INTO channels (channel_id, channel) VALUES(%s, %s)""", ("0", "#PopeTheThird"))
                cur.execute("""INSERT INTO users(user_id, username, is_admin) VALUES(%s, %s, %s)""", ("0", "popethethird", "1"))
                cur.execute("""INSERT INTO mods(channel_id, user_id) VALUES(%s, %s)""", ("0", "0"))
                db.commit()

        except Exception as e:
            print("Error inserting stub data")
            print(traceback.format_exc())
        finally:
            db.close()

    def getConnection(self):
        db = MySQLdb.connect(host=Settings.db_host, user=Settings.db_user, passwd=Settings.db_password, db=Settings.db_name)
        return db

    def dropDB(self):
        try:
            db = MySQLdb.connect(host=Settings.db_host, user=Settings.db_user, passwd=Settings.db_password)
            with closing(db.cursor()) as cur:
                cur.execute("DROP DATABASE %s" % Settings.db_name)

                db.commit()

        except Exception as e:
            print("Error dropping DB")
            print(traceback.format_exc())
        finally:
            db.close()

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
                            "(`channel_id` int NOT NULL AUTO_INCREMENT,"
                            "`channel` varchar(128) NOT NULL UNIQUE,"
                            "`enabled` tinyint(1) DEFAULT 1,"
                            "PRIMARY KEY (`channel_id`))")

                cur.execute("CREATE TABLE IF NOT EXISTS `users` "
                            "(`user_id` int NOT NULL AUTO_INCREMENT,"
                            "`username` varchar(128) NOT NULL UNIQUE,"
                            "`is_admin` tinyint(1) DEFAULT 0,"
                            "`first_seen` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
                            "PRIMARY KEY (`user_id`))")

                cur.execute("CREATE TABLE IF NOT EXISTS `disabled_plugins` "
                            "(`plugin` varchar(128) NOT NULL,"
                            "`channel` varchar(128) NOT NULL)")

                cur.execute("CREATE TABLE IF NOT EXISTS `commands` "
                            "(`channel_id` int NOT NULL,"
                            "`key` VARCHAR(128) NOT NULL,"
                            "`value` VARCHAR(1024) NOT NULL,"
                            "PRIMARY KEY (`channel_id`, `key`))")

                cur.execute("CREATE TABLE IF NOT EXISTS `mods` "
                            "(`channel_id` int NOT NULL,"
                            "`user_id` INT NOT NULL,"
                            "PRIMARY KEY (`channel_id`, `user_id`))")

                cur.execute("CREATE TABLE IF NOT EXISTS `settings` "
                            "(`channel_id` int NOT NULL,"
                            "`key` VARCHAR(128) NOT NULL,"
                            "`value` VARCHAR(1024) NOT NULL,"
                            "PRIMARY KEY (`channel_id`, `key`))")

                db.commit()

        except Exception as e:
            print("Error initializing Tables")
            print(traceback.format_exc())
        finally:
            db.close()