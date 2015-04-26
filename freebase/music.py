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

from dsl import *
from refo import Plus, Question
from quepy.dsl import HasKeyword
from quepy.parsing import Lemma, Lemmas, Pos, QuestionTemplate, Particle


class Band(Particle):
    regex = Question(Pos("DT")) + Plus(Pos("NN") | Pos("NNP"))

    def interpret(self, match):
        name = match.words.tokens.title()
        return IsBand() + HasKeyword(name)


class Topic(Particle):
    regex = Pos("JJ") | Pos("NN") | Pos("NNP") | Pos("NNS")

    def interpret(self, match):
        name = match.words.tokens.title()
        return IsMusicTrack() + SongsAboutStuff(name)


class Artist(Particle):
    regex = Question(Pos("DT")) + Plus(Pos("NN") | Pos("NNP") | Pos("IN"))

    def interpret(self, match):
        name = match.words.tokens.title()
        return IsMusicArtist() + HasKeyword(name)


class YearBf(Particle):
    regex = Pos("CD")

    def interpret(self, match):
        year = match.words.tokens
        return IsBeforeYear(year)


class YearAf(Particle):
    regex = Pos("CD")

    def interpret(self, match):
        year = match.words.tokens
        return IsAfterYear(year)


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
        group = GroupOf(_band_name)
        member = IsPerson() + IsMusicArtist() + IsMemberOf(group)
        name = NameOf(member)
        return name, ReturnValue(i, j)


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
        active_years = ActiveYearsOf(_band_name)
        return active_years, ReturnValue(i, j)


class AlbumsWrittenByBandBeforeYear(QuestionTemplate):
    """
    Ex: "albums by Band() before Year()"
    """
    regex = (Lemma("albums") | Lemma("songs")) + (Lemma("write") + Lemma("by") | Lemma("by")) + Band() + Lemma("before") \
            + YearBf()

    def interpret(self, match):
        _band_name, i, j = match.band
        release_date, i1, j1 = match.yearbf
        album = _band_name + ArtistAlbum(release_date)
        return album, ReturnValue(i, j)


class AlbumsWrittenByBandAfterYear(QuestionTemplate):
    """
    Ex: "albums by Band() before Year()"
    """
    regex = (Lemma("albums") | Lemma("songs")) + (Lemma("write") + Lemma("by") | Lemma("by")) + Band() + Lemma("after") \
            + YearAf()

    def interpret(self, match):
        _band_name, i, j = match.band
        release_date, i1, j1 = match.yearaf
        album = _band_name + ArtistAlbum(release_date)
        return album, ReturnValue(i, j)


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
        name = NameOf(genre)
        return name, ReturnValue(i, j)


class SongsAboutStuffQuestion(QuestionTemplate):
    """
    Ex: "List songs about love"
        "Songs about love"
    """
    regex = (Question(Lemma("list")) + Lemma("songs") + Pos("IN") + Topic()) | (Lemma("love") + Lemma("songs"))

    def interpret(self, match):
        _song, i, j = match.topic
        return _song, ReturnValue(i, j)


class SongsAboutStuffWrittenByPersonQuestion(QuestionTemplate):
    """
    Ex: "List songs about love"
        "Songs about love"
    """
    regex = Question(Lemma("list")) + Lemma("songs") + Pos("IN") + Topic() + (
        Lemma("write by") | Lemma("by")) + Artist()

    def interpret(self, match):
        _song, i, j = match.topic
        _artist, i, j = match.artist
        rezultat = _song + _artist
        return rezultat, ReturnValue(i, j)


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


