from refo import Plus, Question
from quepy.dsl import HasKeyword
from quepy.parsing import Lemma, Pos, QuestionTemplate, Particle
from dsl import *

nouns = Plus(Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))


class Location(Particle):
    regex = Plus(Pos("DT") | Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))

    def interpret(self, match):
        name = match.words.tokens.title()
        return IsLocation() + HasKeyword(name)


class ConflictThatTookPlaceInCountry(QuestionTemplate):
    regex = Question(Lemma("list")) + (Lemma("conflict") | Lemma("conflicts")) + (Lemma("that") | Lemma("which")) +\
        Lemma("took") + Lemma("place") + Pos("IN") + Location()

    def interpret(self, match):
        _location, i, j = match.location
        _military_conflict = IsMilitaryConflict()
        rezultat = _location + IsEvent(_military_conflict)
        return rezultat, ReturnValue(i, j)