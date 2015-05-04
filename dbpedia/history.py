from refo import Plus, Question
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
    regex = (Lemma("weapon") | Lemma("weapons")) + Lemma("use") + Lemma("by") + Country() + Lemma(
        "in") + MilitaryConflict()

    def interpret(self, match):
        _military_conflict, i, j = match.militaryconflict
        _country, i1, j1 = match.country
        rezultat = UsedInWar(_military_conflict) + UsedByCountry(_country)
        return rezultat, ReturnValue(i, j)


class ConflictThatTookPlaceInCountry(QuestionTemplate):
    regex = Question(Lemma("list")) + (Lemma("conflict") | Lemma("conflicts")) + (
        Lemma("that") | Lemma("which")) + Lemma("took") + Lemma("place") + Pos("IN") + Location()

    def interpret(self, match):
        _location, i, j = match.location
        _military_conflict = IsMilitaryConflict()
        rezultat = _military_conflict + ConflictLocation(_location)
        return rezultat, ReturnValue(i, j)


class PersonThatTookPartInConflict(QuestionTemplate):
    regex = Question(Lemma("list")) + (Lemma("person") | Lemma("persons") | Lemma("people")) + (
        Pos("WP") | Pos("WDT")) + (
        (Lemma("was") + Lemma("involved")) | (Lemma("took") + Lemma("part")) | Lemma("fight") | Lemma(
            "fought")) + Pos("IN") + MilitaryConflict()

    def interpret(self, match):
        military_conflict, i, j = match.militaryconflict
        rezultat = IsPerson() + PartOfBattle(military_conflict)
        return rezultat, ReturnValue(i, j)


class PersonThatTookPartInConflictNationality(QuestionTemplate):
    regex = Question(Lemma("list")) + (Lemma("person") | Lemma("persons") | Lemma("people")) + (
        Pos("WP") | Pos("WDT")) + (
        (Lemma("was") + Lemma("involved")) | (Lemma("took") + Lemma("part")) | Lemma("fight") | Lemma(
            "fought")) + Pos(
        "IN") + MilitaryConflict() + (Pos("WP") | Pos("WDT")) + Lemma("be") + (
                Lemma("from") | Lemma("bear") + Pos("IN")) + Country()

    def interpret(self, match):
        military_conflict, i, j = match.militaryconflict
        _nationality, i1, j1 = match.country
        rezultat = IsPerson() + PartOfBattle(military_conflict) + HasBirthPlace(_nationality)
        return rezultat, ReturnValue(i, j)