__author__ = 'Ryan'
from database.SQLHelper import SQLHelper
from database.BaseQueryHelper import BaseQueryHelper
from plugins.LoggingPlugin.LoggingQueryHelper import LoggingQueryHelper
from contextlib import closing
import traceback
from objects.bet import Bet
from objects.game import Game


class GameQueryHelper():
    def __init__(self):
        self.queryHelper = BaseQueryHelper()
        self.loggingQueryHelper = LoggingQueryHelper()
        self.sqlHelper = SQLHelper()
        self.initTables()

    def initTables(self):
        try:
            db = self.sqlHelper.getConnection()
            with closing(db.cursor()) as cur:
                cur.execute("CREATE TABLE IF NOT EXISTS `bets` "
                    "(`bet_id` int NOT NULL AUTO_INCREMENT,"
                    "`channel_id` int NOT NULL,"
                    "`user_id` int NOT NULL,"
                    "`status` ENUM('active', 'complete') DEFAULT 'active',"
                    "`match_id` INT NOT NULL,"
                    "`bet_for` int,"
                    "`bet_amount` double DEFAULT 0,"
                    "PRIMARY KEY (`bet_id`))")

                cur.execute("CREATE TABLE IF NOT EXISTS `complete_matches` "
                    "(`match_id` int NOT NULL AUTO_INCREMENT,"
                    "`url` text,"
                    "`game` text,"
                    "`opponent1` text,"
                    "`opponent2` text,"
                    "`bet1` text,"
                    "`bet2` text,"
                    "`score` text,"
                    "PRIMARY KEY (`match_id`))")
                db.commit()

        except Exception as e:
            print("Error initializing gaming tables")
            print(traceback.format_exc())
        finally:
            db.close()

    def insertComplete(self, game):
        try:
            db = self.sqlHelper.getConnection()
            with closing(db.cursor()) as cur:
                cur.execute("""INSERT IGNORE INTO `complete_matches` (`match_id`, `url`, `game`, `opponent1`, `opponent2`, `bet1`, `bet2`, `score`)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s)""", (game.id, game.link, game.game, game.opp1.encode("UTF-8"), game.opp2.encode("UTF-8"), game.bet1, game.bet2, game.score))
                db.commit()

        except Exception as e:
            print("Error inserting new match archive %s %s %s" % (game.opp1, game.opp2, game.link))
            print(traceback.format_exc())
        finally:
            db.close()

    def insertBet(self, bet, teamNum, match, username, channel):
        try:
            db = self.sqlHelper.getConnection()
            with closing(db.cursor()) as cur:
                channel_id = self.queryHelper.getChannelID(channel)
                user_id = self.queryHelper.getUserID(username)

                cur.execute("""INSERT IGNORE INTO `bets` (`channel_id`, `user_id`, `match_id`, `bet_for`, `bet_amount`)
                VALUES(%s, %s, %s, %s, %s)""", (channel_id, user_id, match.id, teamNum, bet))
                db.commit()

                self.loggingQueryHelper.deductPoints(username, channel, bet)

        except Exception as e:
            print("Error inserting new bet")
            print(traceback.format_exc())
        finally:
            db.close()

    def getBets(self, username, channel, status):
        bets = []
        try:
            db = self.sqlHelper.getConnection()

            with closing(db.cursor()) as cur:
                channel_id = self.queryHelper.getChannelID(channel)
                user_id = self.queryHelper.getUserID(username)

                cur.execute("""SELECT * FROM `bets` WHERE `channel_id` = %s AND `user_id` = %s AND `status` = %s""", (channel_id, user_id, status))
                rows = cur.fetchall()

                for row in rows:
                    bets.append(Bet(row))

        except Exception as e:
            print(traceback.format_exc())
        finally:
            db.close()
            return bets

    def getAllActiveBets(self):
        bets = []
        try:
            db = self.sqlHelper.getConnection()

            with closing(db.cursor()) as cur:

                cur.execute("""SELECT * FROM `bets` WHERE `status` = %s""", ('active',))
                rows = cur.fetchall()

                for row in rows:
                    bets.append(Bet(row))

        except Exception as e:
            print(traceback.format_exc())
        finally:
            db.close()
            return bets

    def getCompletedGame(self, matchID):
        game = None
        try:
            db = self.sqlHelper.getConnection()

            with closing(db.cursor()) as cur:
                cur.execute("""SELECT * FROM `complete_matches` WHERE `match_id` = %s""", (matchID,))

                result = cur.fetchone()
                if not result is None:
                    game = Game(result[2], result[0], "Recent", result[1], result[3], result[4], result[5], result[6])
                    game.setScore(result[7])

        except Exception as e:
            print(traceback.format_exc())
        finally:
            db.close()
            return game

    def setComplete(self, betID):
        try:
            db = self.sqlHelper.getConnection()
            with closing(db.cursor()) as cur:

                cur.execute("""UPDATE `bets` SET `status` = %s WHERE `bet_id` = %s""", ('complete', betID))

                db.commit()

        except Exception as e:
            print("Error updating match status")
            print(traceback.format_exc())
        finally:
            db.close()

    def isMod(self, username, channel):
        return self.queryHelper.isMod(username, channel)

    def isAdmin(self, username):
        return self.queryHelper.isAdmin(username)

    def getPoints(self, username, channel):
        return self.loggingQueryHelper.getPoints(username, channel)

    def deductPoints(self, user_id, channel_id, points):
        username = self.queryHelper.getUsername(user_id)
        channel = self.queryHelper.getChannel(channel_id)

        self.loggingQueryHelper.deductPoints(username, channel, points)

    def increasePoints(self, user_id, channel_id, points):
        username = self.queryHelper.getUsername(user_id)
        channel = self.queryHelper.getChannel(channel_id)

        self.loggingQueryHelper.increasePoints(username, channel, points)