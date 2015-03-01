__author__ = 'Ryan'
from database.SQLHelper import SQLHelper
from database.BaseQueryHelper import BaseQueryHelper
from plugins.LoggingPlugin.LoggingQueryHelper import LoggingQueryHelper
from contextlib import closing
import traceback
from objects.trivia import Trivia
from random import randint
import difflib

class TriviaQueryHelper():
    def __init__(self):
        self.queryHelper = BaseQueryHelper()
        self.loggingQueryHelper = LoggingQueryHelper()
        self.sqlHelper = SQLHelper()
        self.initTables()

    def initTables(self):
        try:
            db = self.sqlHelper.getConnection()
            with closing(db.cursor()) as cur:
                cur.execute("CREATE TABLE IF NOT EXISTS `trivia_categories` "
                    "(`category_id` INT NOT NULL AUTO_INCREMENT,"
                    "`name` TEXT,"
                    "`description` TEXT,"
                    "PRIMARY KEY (`category_id`))")

                cur.execute("CREATE TABLE IF NOT EXISTS `trivia_questions` "
                    "(`question_id` INT NOT NULL AUTO_INCREMENT,"
                    "`category_id` INT,"
                    "`question` TEXT,"
                    "`answer` TEXT,"
                    "`value` INT DEFAULT 0,"
                    "PRIMARY KEY (`question_id`))")

                cur.execute("CREATE TABLE IF NOT EXISTS `trivia_categories_suggestions` "
                    "(`suggestion_id` INT NOT NULL AUTO_INCREMENT,"
                    "`name` TEXT,"
                    "`description` TEXT,"
                    "`user_id` TEXT,"
                    "`channel_id` TEXT,"
                    "`timestamp` DATETIME DEFAULT CURRENT_TIMESTAMP,"
                    "PRIMARY KEY (`suggestion_id`))")

                cur.execute("CREATE TABLE IF NOT EXISTS `trivia_question_suggestions` "
                    "(`suggestion_id` INT NOT NULL AUTO_INCREMENT,"
                    "`category` TEXT,"
                    "`question` TEXT,"
                    "`answer` TEXT,"
                    "`value` INT DEFAULT 0,"
                    "`user_id` TEXT,"
                    "`channel_id` TEXT,"
                    "`timestamp` DATETIME DEFAULT CURRENT_TIMESTAMP,"
                    "PRIMARY KEY (`suggestion_id`))")
                db.commit()

        except Exception as e:
            print("Error initializing trivia tables")
            print(traceback.format_exc())
        finally:
            db.close()

    def isMod(self, username, channel):
        return self.queryHelper.isMod(username, channel)

    def isAdmin(self, username):
        return self.queryHelper.isAdmin(username)

    def getPoints(self, username, channel):
        return self.loggingQueryHelper.getPoints(username, channel)

    def deductPoints(self, username, channel, points):
        self.loggingQueryHelper.deductPoints(username, channel, points)

    def increasePoints(self, username, channel, points):
        self.loggingQueryHelper.increasePoints(username, channel, points)

    def insertCategorySuggestion(self, username, channel, name, description):
        try:
            db = self.sqlHelper.getConnection()
            with closing(db.cursor()) as cur:
                channel_id = self.queryHelper.getChannelID(channel)
                user_id = self.queryHelper.getUserID(username)

                cur.execute("""INSERT IGNORE INTO `trivia_categories_suggestions` (`channel_id`, `user_id`, `name`, `description`)
                VALUES(%s, %s, %s, %s)""", (channel_id, user_id, name, description))
                db.commit()

        except Exception as e:
            print("Error inserting new category suggestion")
            print(traceback.format_exc())
        finally:
            db.close()

    def insertCategory(self, name, description):
        try:
            db = self.sqlHelper.getConnection()
            with closing(db.cursor()) as cur:

                cur.execute("""INSERT IGNORE INTO `trivia_categories` (`name`, `description`)
                VALUES(%s, %s)""", (name, description))
                db.commit()

        except Exception as e:
            print("Error inserting new category")
            print(traceback.format_exc())
        finally:
            db.close()

    def insertQuestionSuggestion(self, username, channel, category, question, answer, value):
        try:
            db = self.sqlHelper.getConnection()
            with closing(db.cursor()) as cur:
                channel_id = self.queryHelper.getChannelID(channel)
                user_id = self.queryHelper.getUserID(username)

                cur.execute("""INSERT IGNORE INTO `trivia_question_suggestions` (`channel_id`, `user_id`, `category`, `question`, `answer`, `value`)
                VALUES(%s, %s, %s, %s, %s, %s)""", (channel_id, user_id, category, question, answer, value))
                db.commit()

        except Exception as e:
            print("Error inserting new question suggestion")
            print(traceback.format_exc())
        finally:
            db.close()

    def findCategoryID(self, category):
        categories = []
        result = -1
        try:
            db = self.sqlHelper.getConnection()

            with closing(db.cursor()) as cur:

                cur.execute("""SELECT category_id, name FROM `trivia_categories`""")
                rows = cur.fetchall()

                for row in rows:
                    categories.append( { "id":row[0], "name":row[1].encode("UTF-8") } )

                sortedList = sorted(categories, key=lambda x: difflib.SequenceMatcher(None, x['name'], category).ratio(), reverse=True)
                print(sortedList)
                result = sortedList[0]['id']

        except Exception as e:
            print(traceback.format_exc())
        finally:
            db.close()
            return result

    def insertQuestion(self, category, question, answer, value):
        try:
            db = self.sqlHelper.getConnection()
            with closing(db.cursor()) as cur:
                category_id = self.findCategoryID(category)

                cur.execute("""INSERT IGNORE INTO `trivia_questions` (`category_id`, `question`, `answer`, `value`)
                VALUES(%s, %s, %s, %s)""", (category_id, question, answer, value))
                db.commit()

        except Exception as e:
            print("Error inserting new question")
            print(traceback.format_exc())
        finally:
            db.close()

    def getRandomQuestion(self):
        question = None
        try:
            db = self.sqlHelper.getConnection()

            with closing(db.cursor()) as cur:

                cur.execute("""SELECT question_id FROM `trivia_questions`""")
                questionIDList = cur.fetchall()


                rand = randint(0, len(questionIDList) - 1)

                cur.execute("""SELECT * FROM `trivia_questions` WHERE `question_id` = %s""", (questionIDList[rand][0],))
                result = cur.fetchone()

                question = Trivia(result[0], result[1], result[2], result[3], result[4])

        except Exception as e:
            print(traceback.format_exc())
        finally:
            db.close()
            return question