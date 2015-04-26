from refo import Plus, Question
from quepy.dsl import HasKeyword
from quepy.parsing import Lemma, Lemmas, Pos, QuestionTemplate, Particle
from dsl import *

nouns = Plus(Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))


class MilitaryConflict(Particle):
    regex = Question(Pos("DT")) + nouns

    def interpret(self, match):
        name = match.words.tokens
        return IsMilitaryConflict() + LabelOfFixedDataRelation(name)


class Country(Particle):
    regex = Plus(Pos("DT") | Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))

    def interpret(self, match):
        name = match.words.tokens.title()
        return IsCountry() + HasKeyword(name)


class Location(Particle):
    regex = Plus(Pos("DT") | Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))

    def interpret(self, match):
        name = match.words.tokens.title()
        return IsPlace() + HasKeyword(name)


class WeaponUsedByCountryInConflict(QuestionTemplate):
    regex = Lemma("weapon") + Lemma("use") + Lemma("by") + Country() + Lemma("in") + MilitaryConflict()

    def interpret(self, match):
        _military_conflict, i, j = match.militaryconflict
        _country, i1, j1 = match.country
        rezultat = UsedInWar(_military_conflict) + UsedByCountry(_country)
        return rezultat, ReturnValue(i, j)


class ConflictThatTookPlaceInCountry(QuestionTemplate):
    regex = Question(Lemma("list")) + (Lemma("conflict") | Lemma("conflicts")) + (Lemma("that") | Lemma("which")) +\
        Lemma("took") + Lemma("place") + Pos("IN") + Location()

    def interpret(self, match):
        _location, i, j = match.location
        _military_conflict = IsMilitaryConflict()
        rezultat = _military_conflict + ConflictLocation(_location)
        return rezultat, ReturnValue(i, j)
