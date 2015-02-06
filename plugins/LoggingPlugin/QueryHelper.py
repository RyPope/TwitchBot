__author__ = 'Ryan'
from database.SQLHelper import SQLHelper
from contextlib import closing
import traceback

class QueryHelper():
    def __init__(self):
        self.sqlHelper = SQLHelper()

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