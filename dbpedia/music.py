# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
# Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

"""
Music related regex
"""

from refo import Plus, Question
from quepy.dsl import HasKeyword
from quepy.parsing import Lemma, Lemmas, Pos, QuestionTemplate, Particle
from dsl import IsBand, LabelOf, IsMemberOf, ActiveYears, MusicGenreOf, \
    NameOf, IsAlbum, ProducedBy, ReturnValue, LabelOfFixedDataRelation, ArtistOf, IsSong, \
    PartOfAlbum


class Album(Particle):
    regex = Plus(Pos("NN") | Pos("NNPS") | Pos("DT") | Pos("NNP"))

    def interpret(self, match):
        name = match.words.tokens.title()
        return LabelOfFixedDataRelation(name)


class Band(Particle):
    regex = Question(Pos("DT")) + Plus(Pos("NN") | Pos("NNP"))

    def interpret(self, match):
        name = match.words.tokens.title()
        return IsBand() + HasKeyword(name)


class BandName(Particle):
    regex = Question(Pos("DT")) + Plus(Pos("NN") | Pos("NNP"))

    def interpret(self, match):
        name = match.words.tokens.title()
        return LabelOfFixedDataRelation(name)


class BandMembersQuestion(QuestionTemplate):
    """
    Regex for questions about band member.
    Ex: "Radiohead members"
        "What are the members of Metallica?"
    """

    regex1 = Band() + Lemma("member")
    regex2 = Lemma("member") + Pos("IN") + Band()
    regex3 = Pos("WP") + Lemma("be") + Pos("DT") + Lemma("member") + \
             Pos("IN") + Band()

    regex = (regex1 | regex2 | regex3) + Question(Pos("."))

    def interpret(self, match):
        _band_name, i, j = match.band
        member = IsMemberOf(_band_name)
        label = LabelOf(member)
        return label, ReturnValue(i, j)


class FoundationQuestion(QuestionTemplate):
    """
    Regex for questions about the creation of a band.
    Ex: "When was Pink Floyd founded?"
        "When was Korn formed?"
    """

    regex = Pos("WRB") + Lemma("be") + Band() + \
            (Lemma("form") | Lemma("found")) + Question(Pos("."))

    def interpret(self, match):
        _band_name, i, j = match.band
        active_years = ActiveYears(_band_name)
        return active_years, ReturnValue(i, j)


class GenreQuestion(QuestionTemplate):
    """
    Regex for questions about the genre of a band.
    Ex: "What is the music genre of Gorillaz?"
        "Music genre of Radiohead"
    """

    optional_opening = Question(Pos("WP") + Lemma("be") + Pos("DT"))
    regex = optional_opening + Question(Lemma("music")) + Lemma("genre") + \
            Pos("IN") + Band() + Question(Pos("."))

    def interpret(self, match):
        _band_name, i, j = match.band
        genre = MusicGenreOf(_band_name)
        label = LabelOf(genre)
        return label, ReturnValue(i, j)


class AlbumsOfQuestion(QuestionTemplate):
    """
    Ex: "List albums of Pink Floyd"
        "What albums did Pearl Jam record?"
        "Albums by Metallica"
    """

    regex = (Question(Lemma("list")) + (Lemma("album") | Lemma("albums")) + \
             Pos("IN") + Band()) | \
            (Lemmas("what album do") + Band() +
             (Lemma("record") | Lemma("make")) + Question(Pos("."))) | \
            (Lemma("list") + Band() + Lemma("album"))

    def interpret(self, match):
        _band_name, i, j = match.band
        album = IsAlbum() + ProducedBy(_band_name)
        name = NameOf(album)
        return name, ReturnValue(i, j)


class SongNameFromAlbumByBand(QuestionTemplate):
    """
    Ex: "what are the names of the tracks on the album Synchronicity by The Police?"
    """
    regex = (((Lemma("what") + Lemma("be")) | Lemma("list")) + Lemma("the") + Lemma("names") + Lemma("of") + Lemma(
        "the") + (Lemma("track") | Lemma("song") | Lemma("songs")) + (
                 (Lemma("on") + Lemma("the")) | Lemma("from")) + Lemma("album") + Album() + (
                 Lemma("write") + Lemma("by") | Lemma("by")) + Band() + Question(Pos("."))) | (
                Lemma("album") + Album() + (Lemma("write") + Lemma("by") | Lemma("by")) + Band())

    def interpret(self, match):
        _album, i, j = match.album
        _band_name, i1, j1 = match.band
        result = _band_name + ArtistOf(IsSong() + PartOfAlbum(_album))
        return result, ReturnValue(i, j)


class SongNameByBand(QuestionTemplate):
    regex = (((Lemma("what") + Lemma("be")) | Lemma("list")) + Lemma("the") + Lemma("names") + Lemma("of") + Lemma(
        "the") + (Lemma("track") | Lemma("song") | Lemma("songs")) + (
        Lemma("write") + Lemma("by") | Lemma("by")) + Band() + Question(Pos("."))) | (
                (Lemma("track") | Lemma("song") | Lemma("songs")) + (
                    Lemma("write") + Lemma("by") | Lemma("by")) + Band() + Question(Pos(".")))

    def interpret(self, match):
        _band_name, i, j = match.band
        result = _band_name + ArtistOf(IsSong())
        return result, ReturnValue(i, j)