# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
#          Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

"""
People related regex
"""

from refo import Plus, Question
from quepy.dsl import HasKeyword, FixedRelation
from quepy.parsing import Lemma, Lemmas, Pos, QuestionTemplate, Particle
from dsl import *
from refo import *

class HasType(FixedRelation):
    relation = "rdf:type"

class Person(Particle):
    regex = Plus(Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))

    def interpret(self, match):
        name = match.words.tokens
        return IsPerson() + HasKeyword(name)


class WhoIs(QuestionTemplate):
    """
    Ex: "Who is Tom Cruise?"
    """

    regex = Lemma("who") + Lemma("be") + Person() + \
        Question(Pos("."))

    def interpret(self, match):
        person_name, i, j = match.person
        definition = DefinitionOf(person_name)
        return definition, "define"


class HowOldIsQuestion(QuestionTemplate):
    """
    Ex: "How old is Bob Dylan".
    """

    regex = Pos("WRB") + Lemma("old") + Lemma("be") + Person() + \
        Question(Pos("."))

    def interpret(self, match):
        person_name, i, j = match.person
        birth_date = BirthDateOf(person_name)
        return birth_date, "age"


class WhereIsFromQuestion(QuestionTemplate):
    """
    Ex: "Where is Bill Gates from?"
    """

    regex = Lemmas("where be") + Person() + Lemma("from") + \
        Question(Pos("."))

    def interpret(self, match):
        person_name, i, j = match.person
        birth_place = BirthPlaceOf(person_name)
        label = LabelOf(birth_place)

        return label, ReturnValue(i, j)

class WhoAreParentsOfQuestion(QuestionTemplate):
    """
    EX: "Who are the parents of Bill Gates"
    """

    regex = Lemma("who") + Lemma("be") + Pos("DT") + Lemma("parent") + Pos("IN") + Person() + \
        Question(Pos(".")) | Lemma("parent") + Pos("IN") + Person() + Question(Pos("."))

    def interpret(self, match):
        parents_name, i, j = match.person
        parents_name = HasParents(parents_name)
        return parents_name, ReturnValue(i, j)

class WhoAreChildrensOfQuestion(QuestionTemplate):
    """
    EX: "Who are the children of Bill Gates"
    """
    regex = Lemma("who") + Lemma("be") + Pos("DT") + Lemma("child") + Pos("IN") + Person() + \
        Question(Pos(".")) | Lemma("child") + Pos("IN") + Person() + Question(Pos("."))

    def interpret(self, match):
        _person, i, j = match.person
        child_name = HasChild(_person)
        return child_name, ReturnValue(i, j)

"""
    ***************** new stuff here ***********
"""

class ReturnValue(object):
    def __init__(self, i, j):
        self.i = i
        self.j = j