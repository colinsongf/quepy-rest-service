# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
# Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

"""
Basic questions for DBpedia.
"""

from refo import Group, Plus, Question
from quepy.parsing import Lemma, Pos, QuestionTemplate, Token, Particle, \
    Lemmas
from quepy.dsl import HasKeyword, IsRelatedTo, HasType
from dsl import DefinitionOf, LabelOf, IsPlace, \
    UTCof, LocationOf, ReturnValue


# Openings
LISTOPEN = Lemma("list") | Lemma("name")


class Thing(Particle):
    regex = Question(Pos("JJ")) + (Pos("NN") | Pos("NNP") | Pos("NNS")) | Pos("VBN")

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


class ListEntity(QuestionTemplate):
    """
    Regex for questions like "List Microsoft software"
    """

    entity = Group(Pos("NNP"), "entity")
    target = Group(Pos("NN") | Pos("NNS"), "target")
    regex = LISTOPEN + entity + target

    def interpret(self, match):
        _entity, i, j = match.entity
        entity = HasKeyword(_entity.tokens)
        _target_type, i1, j1 = match.target
        target_type = HasKeyword(_target_type.lemmas)
        target = HasType(target_type) + IsRelatedTo(entity)
        label = LabelOf(target)

        return label, ReturnValue(i, j)


class WhatTimeIs(QuestionTemplate):
    """
    Regex for questions about the time
    Ex: "What time is it in Cordoba"
    """

    nouns = Plus(Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))
    place = Group(nouns, "place")
    openings = (Lemma("what") +
                ((Token("is") + Token("the") + Question(Lemma("current")) +
                  Question(Lemma("local")) + Lemma("time")) |
                 (Lemma("time") + Token("is") + Token("it")))) | \
               Lemma("time")
    regex = openings + Pos("IN") + place + Question(Pos("."))

    def interpret(self, match):
        _place, i, j = match.place
        place = HasKeyword(_place.lemmas.title()) + IsPlace()
        utc_offset = UTCof(place)

        return utc_offset, ReturnValue(i, j)


class WhereIsQuestion(QuestionTemplate):
    """
    Ex: "where in the world is the Eiffel Tower"
    """

    thing = Group(Plus(Pos("IN") | Pos("NP") | Pos("NNP") | Pos("NNPS")),
                  "thing")
    regex = Lemma("where") + Question(Lemmas("in the world")) + Lemma("be") + \
            Question(Pos("DT")) + thing + Question(Pos("."))

    def interpret(self, match):
        _things, i, j = match.thing
        thing = HasKeyword(_things.tokens)
        location = LocationOf(thing)
        location_name = LabelOf(location)

        return location_name, ReturnValue(i, j)
