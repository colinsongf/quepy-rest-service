# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
# Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

"""
Domain specific language of freebase app.
"""

from quepy.dsl import FixedType, FixedRelation, FixedDataRelation, HasKeyword, FixedRelationDataExtract

# Setup the Keywords for this application
HasKeyword.relation = "/type/object/name"
HasKeyword.language = None
# Setup Fixed Type
FixedType.fixedtyperelation = "/type/object/type"


class NameOf(FixedRelation):
    relation = "/type/object/name"
    reverse = True


class HasName(FixedDataRelation):
    relation = "/type/object/name"


class HasNationality(FixedDataRelation):
    relation = "/people/person/nationality"


class MilitaryCommander(FixedRelation):
    relation = "military_commander"


class GovernmentPosition(FixedDataRelation):
    relation = "/government/government_position_held/basic_title"


class GovernmentPositionJusridiction(FixedRelation):
    relation = "/government/government_position_held/jurisdiction_of_office"


class IsCountry(FixedType):
    fixedtype = "/location/country"


class HoldsGovernmentPosition(FixedRelation):
    relation = "/government/government_position_held/office_holder"
    reverse = True


class DefinitionOf(FixedRelation):
    # relation = "/common/topic/description"
    relation = "id"
    reverse = True


class HasId(FixedRelationDataExtract):
    relation = "id"


class IsPerson(FixedType):
    fixedtype = "/people/person"
    fixedtyperelation = "/type/object/type"


class BirthDateOf(FixedRelation):
    relation = "/people/person/date_of_birth"
    reverse = True


class BirthPlaceOf(FixedRelation):
    relation = "/people/person/place_of_birth"
    reverse = True


class IsMovie(FixedType):
    fixedtype = "/film/film"


class FilmWriteBy(FixedRelation):
    relation = " /film/film/written_by"


class IsMilitaryConflict(FixedType):
    fixedtype = "/military/military_conflict"


class IsEvent(FixedRelation):
    relation = "/location/location/events"
    reverse = True


class IsCommander(FixedRelation):
    relation = "/military/military_conflict/commanders"


class IsMilitaryPersonnelInvolved(FixedRelation):
    relation = "/military/military_conflict/military_personnel_involved"


class DurationOf(FixedRelation):
    relation = "/film/film_cut/runtime"
    reverse = True


class RuntimeOf(FixedRelation):
    relation = "/film/film/runtime"
    reverse = True


class IsActor(FixedType):
    fixedtype = "Actor"
    fixedtyperelation = "/people/person/profession"


class IsPolitician(FixedType):
    fixedtype = "Politician"
    fixedtyperelation = "/people/person/profession"


class IsDirector(FixedType):
    fixedtype = "Film Director"
    fixedtyperelation = "/people/person/profession"


class HasPerformance(FixedRelation):
    relation = "/film/film/starring"


class PerformsIn(FixedRelation):
    relation = "/film/performance/actor"
    reverse = True


class IsPerformance(FixedType):
    fixedtype = "/film/performance"


class PerformanceOfActor(FixedRelation):
    relation = "/film/performance/actor"


class PerformanceOfMovie(FixedRelation):
    relation = "/film/film/starring"
    reverse = True


class DirectorOf(FixedRelation):
    relation = "/film/film/directed_by"
    reverse = True


class DirectedBy(FixedRelation):
    relation = "/film/film/directed_by"


class ReleaseDateOf(FixedRelation):
    relation = "/film/film/initial_release_date"
    reverse = True


class IsBand(FixedType):
    fixedtype = "/music/musical_group"


class IsMusicArtist(FixedType):
    fixedtype = "/music/artist"


class EducationUniversity(FixedRelation):
    relation = "/people/person/education"


class InstitutionEducation(FixedRelation):
    relation = "/education/education/institution"


class IsMemberOf(FixedRelation):
    relation = "/music/group_member/membership"


class GroupOf(FixedRelation):
    relation = "/music/group_membership/group"


class ActiveYearsOf(FixedRelation):
    relation = "/music/artist/active_start"
    reverse = True


class IsMusicGenre(FixedType):
    fixedtype = "/music/genre"


class IsBeforeYear(FixedDataRelation):
    relation = "release_date<="


class IsBornAfterYear(FixedDataRelation):
    relation = "/people/person/date_of_birth>="


class IsBornBeforeYear(FixedDataRelation):
    relation = "/people/person/date_of_birth<="


class IsAfterYear(FixedDataRelation):
    relation = "release_date>="


class EventStartDateAfter(FixedDataRelation):
    relation = "/time/event/start_date>="


class EventStartDateBefore(FixedDataRelation):
    relation = "/time/event/start_date<="


class TrackLengthHigh(FixedDataRelation):
    relation = "/music/release_track/length>="


class MusicGenreOf(FixedRelation):
    relation = "/music/artist/genre"
    reverse = True


class IsAlbum(FixedType):
    fixedtype = "/music/album"


class AlbumArtist(FixedDataRelation):
    relation = "/music/album/artist"


class ArtistAlbum(FixedRelation):
    relation = "/music/artist/album"


class PrimaryRelease(FixedRelation):
    relation = "/music/album/primary_release"


class TrackList(FixedRelation):
    relation = "/music/release/track_list"


class ProducedBy(FixedRelation):
    relation = "/music/artist/album"
    reverse = True


class IsLocation(FixedType):
    fixedtype = "/location/location"


class IsCountry(FixedType):
    fixedtype = "/location/country"


class IsPresident(FixedType):
    fixedtype = "President"
    fixedtyperelation = "/government/government_position_held/basic_title"


class OfficeHolderOf(FixedRelation):
    relation = "/government/government_position_held/office_holder"
    reverse = True


class PresidentOf(FixedRelation):
    relation = "/government/government_position_held/jurisdiction_of_office"


class CapitalOf(FixedRelation):
    relation = "/location/country/capital"
    reverse = True


class LanguageOf(FixedRelation):
    relation = "/location/country/official_language"
    reverse = True


class PopulationOf(FixedRelation):
    relation = "/location/statistical_region/population"
    reverse = True


class NumberOf(FixedRelation):
    relation = "/measurement_unit/dated_integer/number"
    reverse = True


class IsTvShow(FixedType):
    fixedtype = "/tv/tv_program"


class CastOf(FixedRelation):
    relation = "/tv/tv_program/regular_cast"
    reverse = True


class IsActorOf(FixedRelation):
    relation = "/tv/regular_tv_appearance/actor"
    reverse = True


class HasActor(FixedRelation):
    relation = "/tv/regular_tv_appearance/actor"


class HasCast(FixedRelation):
    relation = "/tv/tv_program/regular_cast"


class NumberOfEpisodesIn(FixedRelation):
    relation = "/tv/tv_program/number_of_episodes"
    reverse = True


class CreatorOf(FixedRelation):
    relation = "/tv/tv_program/program_creator"
    reverse = True


class IsBook(FixedType):
    fixedtype = "/book/book"


class IsMusicTrack(FixedType):
    fixedtype = "/music/track"


class AuthorOf(FixedRelation):
    relation = "/book/written_work/author"
    reverse = True


class HasAuthor(FixedRelation):
    relation = "/book/written_work/author"


class LocationOf(FixedRelation):
    relation = "/location/location/containedby"
    reverse = True


class HasParents(FixedRelation):
    relation = "/people/person/parents"
    reverse = True


class HasChild(FixedRelation):
    relation = "/people/person/children"
    reverse = True


class HasImage(FixedDataRelation):
    relation = "/common/topic/image"


class NameApproximation(FixedDataRelation):
    relation = "name~="


class ReturnValue(object):
    def __init__(self, i, j):
        self.i = i
        self.j = j