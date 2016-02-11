__author__ = 'truba'

class TextPeriod:
    def __init__(self):
        self.no = []
        self.yes = None

    def yes_time_span(self):
        parts = self.yes.split('-')
        return int(parts[0]), int(parts[1])

    def no_time_span(self, index):
        parts = self.no[index].split('-')
        return int(parts[0]), int(parts[1])


class TextEntry:
    def __init__(self):
        self.id = None
        self.textF = TextPeriod()
        self.textM = TextPeriod()
        self.textC = TextPeriod()
        self.body = None

    def __str__(self):
        return str(self.body)

    def __repr__(self):
        return self.__str__()


class WordLabel:
    def __init__(self, word, label, percentage):
        self.percentage = percentage
        self.word = word
        self.label = label

    def __str__(self):
        return str(self.word)+" in "+str(self.label)+", p = "+str(self.percentage)
