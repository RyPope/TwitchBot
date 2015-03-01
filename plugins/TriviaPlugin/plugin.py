from plugins.BasePlugin import BasePlugin
from plugins.TriviaPlugin.TriviaQueryHelper import TriviaQueryHelper
import re
import threading
from collections import defaultdict
from objects.trivia import Trivia
import time

class TriviaPlugin(BasePlugin):
    def __init__(self, twitchBot):
        super(TriviaPlugin, self).__init__(twitchBot)
        self.className = self.__class__.__name__

        self.queryHelper = TriviaQueryHelper()

        self.registerCommand(self.className, "suggest", self.suggestHandler)
        self.registerCommand(self.className, "add", self.addHandler)
        self.registerCommand(self.className, "trivia", self.triviaHandler)
        self.registerCommand(self.className, "hint", self.hintHandler)
        self.registerAll(self.className, self.answerHandler)

        self.triviaRunning = []
        self.triviaDict = defaultdict(Trivia)

    def answerHandler(self, username, channel, args):
        if channel in self.triviaRunning and not self.triviaDict[channel] is None:
            answer = " ".join(args).lower().strip()
            if answer == self.triviaDict[channel].answer:
                question = self.triviaDict[channel]
                self.sendMessage(self.className, channel, "%s has answered correctly (\"%s\") and been rewarded %s points" % (username, question.answer, question.value))
                self.queryHelper.increasePoints(username, channel, question.value)
                self.triviaDict[channel] = None

    def hintHandler(self, username, channel, args):
        if channel in self.triviaRunning and not self.triviaDict[channel] is None:
            trivia = self.triviaDict[channel]
            self.sendMessage(self.className, channel, "Question: %s - Hint %s: %s" % (trivia.question, trivia.hint_num, trivia.hint))
        else:
            self.sendMessage(self.className, channel, "Trivia is not currently running or a question has not been asked yet.")

    def triviaLoop(self, channel):
        if channel in self.triviaRunning:
            if self.triviaDict[channel] == None:
                self.triviaDict[channel] = self.queryHelper.getRandomQuestion()
            question = self.triviaDict[channel]
            if question.hint_num > 3:
                self.sendMessage(self.className, channel, "No one got the answer! It was %s" % question.answer)
                question = None
            else:
                if question.hint_num == 0:
                    self.sendMessage(self.className, channel, "Question (%s points): %s" % (self.triviaDict[channel].value, self.triviaDict[channel].question))
                time.sleep(.5)

                self.sendMessage(self.className, channel, "Hint %s: %s" % (question.hint_num, question.getHint()))
                question.hint_num += 1

            self.triviaDict[channel] = question
            threading.Timer(60 * 2, self.triviaLoop, args=(channel,)).start()

    def triviaHandler(self, username, channel, args):
        if not (self.queryHelper.isMod(username, channel) or self.queryHelper.isAdmin(username)):
            self.sendMessage(self.className, channel, "This command is available to mods or admins only.")
        else:
            if args[1].lower() == "start":
                if not channel in self.triviaRunning:
                    self.triviaRunning.append(channel)
                    trivia = self.queryHelper.getRandomQuestion()
                    self.triviaDict[channel] = trivia
                    self.triviaLoop(channel)

            elif args[1].lower() == "stop":
                if channel in self.triviaRunning:
                    self.triviaRunning.remove(channel)
                    self.sendMessage(self.className, channel, "Trivia ended. The answer for \"%s\" was \"%s\"" % (self.triviaDict[channel].question, self.triviaDict[channel].answer))


    def suggestHandler(self, username, channel, args):
        if len(args) < 2:
            self.sendMessage(self.className, channel, "Invalid syntax, please use suggest <category | question>")
        elif args[1].lower() == "category":
            quoted = re.findall('"([^"]*)"', " ".join(args[2:]))
            if not len(quoted) == 2:
                self.sendMessage(self.className, channel, "Invalid syntax, please enter category and category description between seperate double quotes.")
            elif len(args) < 4:
                self.sendMessage(self.className, channel, "Invalid syntax, please use suggest category \"<category name>\" \"<category description>\"")
            else:
                name = quoted[0]
                description = quoted[1]
                self.queryHelper.insertCategorySuggestion(username, channel, name, description)
                self.sendMessage(self.className, channel, "Your suggestion has been logged and will be reviewed shortly.")
        elif args[1].lower() == "question":
            if len(args) < 4:
                self.sendMessage(self.className, channel, "Invalid syntax, please use suggest question \"<category>\" \"<question>\" \"<answer>\" <points>")
            else:
                quoted = re.findall('"([^"]*)"', " ".join(args[2:]))
                points = args[-1]

                if not len(quoted) == 3:
                    self.sendMessage(self.className, channel, "Invalid syntax, please enter category, question and answer between seperate double quotes.")
                elif not points.isdigit() or int(points) <= 0:
                    self.sendMessage(self.className, channel, "Invalid syntax, point value must be positive integer.")
                else:
                    self.queryHelper.insertQuestionSuggestion(username, channel, quoted[0], quoted[1], quoted[2], points)
                    self.sendMessage(self.className, channel, "Your question has been logged and will be reviewed shortly.")

    def addHandler(self, username, channel, args):
        if len(args) < 2:
            self.sendMessage(self.className, channel, "Invalid syntax, please use add <category | question>")
        elif not self.queryHelper.isAdmin(username):
            self.sendMessage(self.className, channel, "This command is available to admins only.")
        elif args[1].lower() == "category":
            if len(args) < 4:
                self.sendMessage(self.className, channel, "Invalid syntax, please use add category <category name> <category description>")
            else:
                name = args[2]
                description = " ".join(args[3:])
                self.queryHelper.insertCategory(name, description)
                self.sendMessage(self.className, channel, "Your suggestion has been added.")
        elif args[1].lower() == "question":
            if len(args) < 4:
                self.sendMessage(self.className, channel, "Invalid syntax, please use add question <category> \"<question>\" \"<answer>\" <points>")
            else:
                category = args[2]
                quoted = re.findall('"([^"]*)"', " ".join(args[3:]))
                points = args[-1]

                if not len(quoted) == 2:
                    self.sendMessage(self.className, channel, "Invalid syntax, please enter question and answer between seperate double quotes.")
                elif not points.isdigit() or int(points) <= 0:
                    self.sendMessage(self.className, channel, "Invalid syntax, point value must be positive integer.")
                else:
                    self.queryHelper.insertQuestion(category, quoted[0], quoted[1], points)
                    self.sendMessage(self.className, channel, "Your question has been added.")