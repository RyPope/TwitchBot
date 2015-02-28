__author__ = 'Ryan'
import re
from random import randint

class Trivia:
    def __init__(self, id, category_id, question, answer, value):
        self.id = int(id)
        self.category_id = int(category_id)
        self.question = question.encode("UTF-8")
        self.answer = answer.encode("UTF-8")
        self.value = int(value)
        self.hint_num = 0
        self.hint = self.getHint()

    def getHint(self):
        if self.hint_num == 0:
            self.hint = re.sub('[0-9a-zA-Z]', '*', self.answer)
        else:
            if not len(self.hint) <= ((self.hint_num - 1) * 2 + 2):
                for i in range(0, 2):
                    rand = randint(0, len(self.hint) - 1)
                    while not self.hint[rand] == "*":
                        rand = randint(0, len(self.hint) - 1)

                    temp = list(self.hint)

                    temp[rand] = self.answer[rand]

                    self.hint = "".join(temp)

        return self.hint
