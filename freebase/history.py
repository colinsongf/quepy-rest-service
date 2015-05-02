from refo import Plus, Question
from quepy.parsing import Lemma, Pos, QuestionTemplate, Particle
from dsl import *

nouns = Plus(Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))


class MilitaryConflict(Particle):
    regex = Question(Pos("DT")) + Plus(nouns | Pos("IN"))

    def interpret(self, match):
        name = match.words.tokens
        return IsMilitaryConflict() + HasName(name)


class Nationality(Particle):
    regex = Question(Pos("DT")) + Plus(nouns | Pos("IN"))

    def interpret(self, match):
        name = match.words.tokens
        return HasNationality(name)


class Location(Particle):
    regex = Plus(Pos("DT") | Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))

    def interpret(self, match):
        name = match.words.tokens.title()
        return IsLocation() + HasKeyword(name)


class YearBf(Particle):
    regex = Pos("CD")

    def interpret(self, match):
        year = match.words.tokens
        return EventStartDateBefore(year)


class YearAf(Particle):
    regex = Pos("CD")

    def interpret(self, match):
        year = match.words.tokens
        return EventStartDateAfter(year)


class BornAfterYear(Particle):
    regex = Pos("CD")

    def interpret(self, match):
        year = match.words.tokens
        return IsBornAfterYear(year)


class BornBeforeYear(Particle):
    regex = Pos("CD")

    def interpret(self, match):
        year = match.words.tokens
        return IsBornBeforeYear(year)


class ConflictThatTookPlaceInCountry(QuestionTemplate):
    regex = Question(Lemma("list")) + (Lemma("conflict") | Lemma("conflicts")) + (Lemma("that") | Lemma("which")) + \
            Lemma("took") + Lemma("place") + Pos("IN") + Location()

    def interpret(self, match):
        _location, i, j = match.location
        _military_conflict = IsMilitaryConflict()
        rezultat = DefinitionOf(_military_conflict + IsEvent(_location))
        return rezultat, ReturnValue(i, j)


class ConflictThatTookPlaceInCountryAfterYear(QuestionTemplate):
    regex = Question(Lemma("list")) + (Lemma("conflict") | Lemma("conflicts")) + (Lemma("that") | Lemma("which")) + \
            Lemma("took") + Lemma("place") + Pos("IN") + Location() + Lemma("after") + YearAf()

    def interpret(self, match):
        _location, i, j = match.location
        _military_conflict = IsMilitaryConflict()
        after_year, i1, j1 = match.yearaf
        rezultat = DefinitionOf(_military_conflict + after_year + IsEvent(_location))
        return rezultat, ReturnValue(i, j)


class ConflictThatTookPlaceInCountryBeforeYear(QuestionTemplate):
    regex = Question(Lemma("list")) + (Lemma("conflict") | Lemma("conflicts")) + (Lemma("that") | Lemma("which")) + \
            Lemma("took") + Lemma("place") + Pos("IN") + Location() + Lemma("before") + YearBf()

    def interpret(self, match):
        _location, i, j = match.location
        _military_conflict = IsMilitaryConflict()
        after_year, i1, j1 = match.yearbf
        rezultat = DefinitionOf(_military_conflict + after_year + IsEvent(_location))
        return rezultat, ReturnValue(i, j)


class PersonThatTookPartInConflict(QuestionTemplate):
    regex = Question(Lemma("list")) + (Lemma("person") | Lemma("persons") | Lemma("people")) + (
        Pos("WP") | Pos("WDT")) + (
        (Lemma("was") + Lemma("involved")) | (Lemma("took") + Lemma("part")) | Lemma("fight") | Lemma(
            "fought")) + Pos(
        "IN") + MilitaryConflict()

    def interpret(self, match):
        military_conflict, i, j = match.militaryconflict
        rezultat = military_conflict + IsCommander(
            MilitaryCommander(HasId() + IsPerson())) + IsMilitaryPersonnelInvolved(
            HasId() + IsPerson())
        return rezultat, ReturnValue(i, j)


class PersonThatTookPartInConflictNationality(QuestionTemplate):
    regex = Question(Lemma("list")) + (Lemma("person") | Lemma("persons") | Lemma("people")) + (
        Pos("WP") | Pos("WDT")) + (
        (Lemma("was") + Lemma("involved")) | (Lemma("took") + Lemma("part")) | Lemma("fight") | Lemma(
            "fought")) + Pos(
        "IN") + MilitaryConflict() + (Pos("WP") | Pos("WDT")) + Lemma("be") + (
                Lemma("from") | Lemma("bear") + Pos("IN")) + Nationality()

    def interpret(self, match):
        military_conflict, i, j = match.militaryconflict
        _nationality, i1, j1 = match.nationality
        rezultat = military_conflict + IsCommander(
            MilitaryCommander(IsPerson() + _nationality + HasId())) + IsMilitaryPersonnelInvolved(
            IsPerson() + _nationality + HasId())
        return rezultat, ReturnValue(i, j)


class PersonThatTookPartInConflictBornAfter(QuestionTemplate):
    regex = Question(Lemma("list")) + (Lemma("person") | Lemma("persons") | Lemma("people")) + (
        Pos("WP") | Pos("WDT")) + (
        (Lemma("was") + Lemma("involved")) | (Lemma("took") + Lemma("part")) | Lemma("fight") | Lemma(
            "fought")) + Pos(
        "IN") + MilitaryConflict() + (Pos("WP") | Pos("WDT")) + Lemma("be") + Lemma("bear") + Lemma(
        "after") + BornAfterYear()

    def interpret(self, match):
        military_conflict, i, j = match.militaryconflict
        _born_year, i1, j1 = match.bornafteryear
        rezultat = military_conflict + IsCommander(IsMilitaryPersonnelInvolved(
            IsPerson() + _born_year + HasId()))
        return rezultat, ReturnValue(i, j)


class PersonThatTookPartInConflictBornBefore(QuestionTemplate):
    regex = Question(Lemma("list")) + (Lemma("person") | Lemma("persons") | Lemma("people")) + (
        Pos("WP") | Pos("WDT")) + (
        (Lemma("was") + Lemma("involved")) | (Lemma("took") + Lemma("part")) | Lemma("fight") | Lemma(
            "fought")) + Pos(
        "IN") + MilitaryConflict() + (Pos("WP") | Pos("WDT")) + Lemma("be") + Lemma("bear") + Lemma(
        "before") + BornBeforeYear()

    def interpret(self, match):
        military_conflict, i, j = match.militaryconflict
        _born_year, i1, j1 = match.bornbeforeyear
        rezultat = military_conflict + IsMilitaryPersonnelInvolved(
            IsPerson() + _born_year + HasId())
        return rezultat, ReturnValue(i, j)


class PersonThatTookPartInConflictNationalityBornAfter(QuestionTemplate):
    regex = Question(Lemma("list")) + (Lemma("person") | Lemma("persons") | Lemma("people")) + (
        Pos("WP") | Pos("WDT")) + (
        (Lemma("was") + Lemma("involved")) | (Lemma("took") + Lemma("part")) | Lemma("fight") | Lemma(
            "fought")) + Pos(
        "IN") + MilitaryConflict() + (Pos("WP") | Pos("WDT")) + Lemma("be") + (
                Lemma("from") | Lemma("bear") + Pos("IN")) + Nationality() + Lemma(
        "after") + BornAfterYear()

    def interpret(self, match):
        military_conflict, i, j = match.militaryconflict
        _nationality, i1, j1 = match.nationality
        _born_year, i2, j2 = match.bornafteryear
        rezultat = military_conflict + IsMilitaryPersonnelInvolved(
            IsPerson() + _born_year + _nationality + HasId())
        return rezultat, ReturnValue(i, j)


class PersonThatTookPartInConflictNationalityBornBefore(QuestionTemplate):
    regex = Question(Lemma("list")) + (Lemma("person") | Lemma("persons") | Lemma("people")) + (
        Pos("WP") | Pos("WDT")) + (
        (Lemma("was") + Lemma("involved")) | (Lemma("took") + Lemma("part")) | Lemma("fight") | Lemma(
            "fought")) + Pos(
        "IN") + MilitaryConflict() + (Pos("WP") | Pos("WDT")) + Lemma("be") + (
                Lemma("from") | Lemma("bear") + Pos("IN")) + Nationality() + Lemma(
        "before") + BornBeforeYear()

    def interpret(self, match):
        military_conflict, i, j = match.militaryconflict
        _nationality, i1, j1 = match.nationality
        _born_year, i2, j2 = match.bornbeforeyear
        rezultat = military_conflict + military_conflict + IsMilitaryPersonnelInvolved(
            IsPerson() + _born_year + _nationality + HasId())
        return rezultat, ReturnValue(i, j)