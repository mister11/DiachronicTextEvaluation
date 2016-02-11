__author__ = 'truba'
import ShifterParser
from ShifterParser import Shifter, ShifterDelegate

class MockEval(ShifterDelegate):

    def evaluate_text(self, text):
        return 1800

shifer = Shifter(ShifterParser.TYPE_TEXT_F, MockEval())

shifer.perform("../data/evaluationScript/goldStandard.txt", "../data/evaluationScript/test_output.txt")