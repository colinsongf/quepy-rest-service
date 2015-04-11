# coding: utf-8

"""
Tv Shows related regex.
"""

from refo import Plus, Question
from quepy.dsl import HasKeyword
from quepy.parsing import Lemma, Lemmas, Pos, QuestionTemplate, Particle
from dsl import IsTvShow, ReleaseDateOf, IsPerson, StarsIn, LabelOf, \
    HasShowName, NumberOfEpisodesIn, HasActor, ShowNameOf, CreatorOf, ReturnValue

nouns = Plus(Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))


class TvShow(Particle):
    regex = Plus(Question(Pos("DT")) + nouns)

    def interpret(self, match):
        name = match.words.tokens
        return IsTvShow() + HasShowName(name)


class Actor(Particle):
    regex = nouns

    def interpret(self, match):
        name = match.words.tokens
        return IsPerson() + HasKeyword(name)


# FIXME: clash with movies release regex
class ReleaseDateQuestion(QuestionTemplate):
    """
    Ex: when was Friends release?
    """

    regex = Lemmas("when be") + TvShow() + Lemma("release") + \
        Question(Pos("."))

    def interpret(self, match):
        tv_show, i, j = match.tvshow
        release_date = ReleaseDateOf(tv_show)
        return release_date, ReturnValue(i, j)


class CastOfQuestion(QuestionTemplate):
    """
    Ex: "What is the cast of Friends?"
        "Who works in Breaking Bad?"
        "List actors of Seinfeld"
    """

    regex = (Question(Lemmas("what be") + Pos("DT")) +
             Lemma("cast") + Pos("IN") + TvShow() + Question(Pos("."))) | \
            (Lemmas("who works") + Pos("IN") + TvShow() +
             Question(Pos("."))) | \
            (Lemmas("list actor") + Pos("IN") + TvShow())

    def interpret(self, match):
        tv_show, i, j = match.tvshow
        actor = IsPerson() + StarsIn(tv_show)
        name = LabelOf(actor)
        return name, ReturnValue(i, j)


class ListTvShows(QuestionTemplate):
    """
    Ex: "List TV shows"
    """

    regex = Lemmas("list tv show")

    def interpret(self, match):
        show = IsTvShow()
        label = LabelOf(show)
        return label, "enum"


class EpisodeCountQuestion(QuestionTemplate):
    """
    Ex: "How many episodes does Seinfeld have?"
        "Number of episodes of Seinfeld"
    """

    regex = ((Lemmas("how many episode do") + TvShow() + Lemma("have")) |
             (Lemma("number") + Pos("IN") + Lemma("episode") +
              Pos("IN") + TvShow())) + \
            Question(Pos("."))

    def interpret(self, match):
        tv_show, i, j = match.tvshow
        number_of_episodes = NumberOfEpisodesIn(tv_show)
        return number_of_episodes, ReturnValue(i, j)


class ShowsWithQuestion(QuestionTemplate):
    """
    Ex: "List shows with Hugh Laurie"
        "In what shows does Jennifer Aniston appears?"
        "Shows with Matt LeBlanc"
    """

    regex = (Lemmas("list show") + Pos("IN") + Actor()) | \
            (Pos("IN") + (Lemma("what") | Lemma("which")) + Lemmas("show do") +
             Actor() + (Lemma("appear") | Lemma("work")) +
             Question(Pos("."))) | \
            ((Lemma("show") | Lemma("shows")) + Pos("IN") + Actor())

    def interpret(self, match):
        _actor, i, j = match.actor
        show = IsTvShow() + HasActor(_actor)
        show_name = ShowNameOf(show)
        return show_name, ReturnValue(i, j)


class CreatorOfQuestion(QuestionTemplate):
    """
    Ex: "Who is the creator of Breaking Bad?"
    """

    regex = Question(Lemmas("who be") + Pos("DT")) + \
        Lemma("creator") + Pos("IN") + TvShow() + Question(Pos("."))

    def interpret(self, match):
        tv_show, i, j = match.tvshow
        creator = CreatorOf(tv_show)
        label = LabelOf(creator)
        return label, ReturnValue(i, j)
