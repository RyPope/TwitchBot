from plugins.BasePlugin import BasePlugin
from plugins.TriviaPlugin.TriviaQueryHelper import TriviaQueryHelper
import re
import threading
from objects.trivia import Trivia

class TriviaPlugin(BasePlugin):
    def __init__(self, twitchBot):
        super(TriviaPlugin, self).__init__(twitchBot)
        self.className = self.__class__.__name__

        self.queryHelper = TriviaQueryHelper()

        self.registerCommand(self.className, "suggest", self.suggestHandler)
        self.registerCommand(self.className, "add", self.addHandler)
        self.registerCommand(self.className, "trivia", self.triviaHandler)

        self.triviaRunning = []

    def triviaLoop(self, channel, question):
        if channel in self.triviaRunning:

            if question.getHintNum() > 3:
                self.sendMessage(self.className, channel, "No one got the answer! It was %s" % question.answer)
                question = self.queryHelper.getRandomQuestion()
            else:
                self.sendMessage(self.className, channel, "Hint %s: %s" % (question.getHintNum(), question.getHint()))

            threading.Timer(15, self.triviaLoop, args=(channel, question)).start()

    def triviaHandler(self, username, channel, args):
        if not self.queryHelper.isMod(username, channel) or not self.queryHelper.isAdmin(username):
            self.sendMessage(self.className, channel, "This command is available to mods or admins only.")
        else:
            if args[1].lower() == "start":
                if not channel in self.triviaRunning:
                    self.sendMessage(self.className, channel, "Trivia started.")
                    self.triviaRunning.append(channel)
                    trivia = self.queryHelper.getRandomQuestion()
                    self.triviaLoop(channel, trivia)
                    print(channel, self.triviaRunning)
            elif args[1].lower() == "stop":
                if channel in self.triviaRunning:
                    self.triviaRunning.remove(channel)
                    self.sendMessage(self.className, channel, "Trivia ended.")


    def suggestHandler(self, username, channel, args):
        if len(args) < 2:
            self.sendMessage(self.className, channel, "Invalid syntax, please use suggest <category | question>")
        elif args[1].lower() == "category":
            if len(args) < 4:
                self.sendMessage(self.className, channel, "Invalid syntax, please use suggest category <category name> <category description>")
            else:
                name = args[2]
                description = " ".join(args[3:])
                self.queryHelper.insertCategorySuggestion(username, channel, name, description)
                self.sendMessage(self.className, channel, "Your suggestion has been logged and will be reviewed shortly.")
        elif args[1].lower() == "question":
            if len(args) < 4:
                self.sendMessage(self.className, channel, "Invalid syntax, please use suggest question <category> \"<question>\" \"<answer>\" <points>")
            else:
                category = args[2]
                quoted = re.findall('"([^"]*)"', " ".join(args[3:]))
                points = args[-1]

                if not len(quoted) == 2:
                    self.sendMessage(self.className, channel, "Invalid syntax, please enter question and answer between seperate double quotes.")
                elif not points.isdigit() or int(points) <= 0:
                    self.sendMessage(self.className, channel, "Invalid syntax, point value must be positive integer.")
                else:
                    self.queryHelper.insertQuestionSuggestion(username, channel, category, quoted[0], quoted[1], points)
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