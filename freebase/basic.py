# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
# Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

"""
Basic questions for Freebase.
"""

from refo import Question, Plus
from dsl import *
from quepy.dsl import HasKeyword
from quepy.parsing import QuestionTemplate, Particle, Lemma, Pos, Lemmas


nouns = Plus(Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))


class Location(Particle):
    regex = Plus(Pos("DT") | nouns)

    def interpret(self, match):
        name = match.words.tokens.title()
        return IsLocation() + HasKeyword(name)


class Movie(Particle):
    regex = Question(Pos("DT")) + nouns

    def interpret(self, match):
        name = match.words.tokens
        return IsMovie() + HasName(name)


class Band(Particle):
    regex = Question(Pos("DT")) + Plus(Pos("NN") | Pos("NNP"))

    def interpret(self, match):
        name = match.words.tokens.title()
        return IsBand() + HasKeyword(name)


class TvShow(Particle):
    regex = Plus(Question(Pos("DT")) + nouns)

    def interpret(self, match):
        name = match.words.tokens
        return IsTvShow() + HasName(name)


class Book(Particle):
    regex = Plus(nouns)

    def interpret(self, match):
        name = match.words.tokens
        return IsBook() + HasKeyword(name)


class MilitaryConflict(Particle):
    regex = Question(Pos("DT")) + Plus(nouns | Pos("IN"))

    def interpret(self, match):
        name = match.words.tokens
        return IsMilitaryConflict() + HasName(name)


class Thing(Particle):
    regex = Plus(Question(Pos("JJ")) + (Pos("NN") | Pos("NNP") | Pos("NNS")) |
                 Pos("VBN"))

    def interpret(self, match):
        return HasKeyword(match.words.tokens)


class WhatIs(QuestionTemplate):
    """
    Regex for questions like "What is a blowtorch
    Ex: "What is a car"
        "What is Seinfield?"
    """

    regex = Lemma("what") + Lemma("be") + Question(Pos("DT")) + \
            Thing() + Question(Pos("."))

    def interpret(self, match):
        _thing, i, j = match.thing
        label = DefinitionOf(_thing)

        return label, ReturnValue(i, j)


class WhereIsQuestion(QuestionTemplate):
    """
    Ex: "where in the world is the Eiffel Tower"
    """

    regex = Lemma("where") + Question(Lemmas("in the world")) + Lemma("be") + \
            Question(Pos("DT")) + Thing() + Question(Pos("."))

    def interpret(self, match):
        _things, i, j = match.thing
        location = LocationOf(_things)
        location_name = NameOf(location)
        return location_name, ReturnValue(i, j)


class WhatIsLocation(QuestionTemplate):
    regex = (Lemma("what") + Lemma("is") + Lemma("location") + Location()) | (
        Lemma("location") + Location())

    def interpret(self, match):
        _location, i, j = match.location
        return _location + HasId(), ReturnValue(i, j)


class WhatIsMovie(QuestionTemplate):
    regex = (Lemma("what") + Lemma("is") + Lemma("movie") + Movie()) | (
        Lemma("movie") + Movie())

    def interpret(self, match):
        _movie, i, j = match.movie
        return _movie + HasId(), ReturnValue(i, j)


class WhatIsTvShow(QuestionTemplate):
    regex = (Lemma("what") + Lemma("is") + Lemma("tv") + Lemma("show") + TvShow()) | (
        Lemma("tv") + Lemma("show") + TvShow())

    def interpret(self, match):
        tv_show, i, j = match.tvshow
        return tv_show + HasId(), ReturnValue(i, j)


class WhatIsBook(QuestionTemplate):
    regex = (Lemma("what") + Lemma("is") + Lemma("book") + Book()) | (
        Lemma("book") + Book())

    def interpret(self, match):
        _book, i, j = match.book
        return _book + HasId(), ReturnValue(i, j)


class WhatIsBand(QuestionTemplate):
    regex = (Lemma("what") + Lemma("is") + Lemma("band") + Band()) | (
        Lemma("band") + Band())

    def interpret(self, match):
        _band, i, j = match.band
        return _band + HasId(), ReturnValue(i, j)


class WhatIsMilitaryConflict(QuestionTemplate):
    regex = (Lemma("what") + Lemma("is") + Lemma("military") + Lemma("conflict") + MilitaryConflict()) | (
        Lemma("military") + Lemma("conflict") + MilitaryConflict())

    def interpret(self, match):
        _military_conflict, i, j = match.militaryconflict
        return _military_conflict + HasId(), ReturnValue(i, j)