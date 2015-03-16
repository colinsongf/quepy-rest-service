# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
#          Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

"""
Implements the Quepy Application API
"""

import logging
import sys
from importlib import import_module
from types import ModuleType

from quepy import settings
from quepy import generation
from quepy.parsing import QuestionTemplate
from quepy.expression import Expression
from quepy.tagger import get_tagger, TaggingError
from quepy.encodingpolicy import encoding_flexible_conversion


logger = logging.getLogger("quepy.quepyapp")


def install(app_name):
    """
    Installs the application and gives an QuepyApp object
    """
    print sys.modules

    """freebase"""

    if 'freebase' in sys.modules:
        #delete_module('freebase')
        del sys.modules['freebase']
    if 'freebase.basic' in sys.modules:
        #delete_module('freebase.basic')
        del sys.modules['freebase.basic']
    if 'freebase.country' in sys.modules:
        #delete_module('freebase.country')
        del sys.modules['freebase.country']
    if 'freebase.tvshows' in sys.modules:
        #delete_module('freebase.tvshows')
        del sys.modules['freebase.tvshows']
    if 'freebase.people' in sys.modules:
        #delete_module('freebase.people')
        del sys.modules['freebase.people']
    if 'freebase.settings' in sys.modules:
        #delete_module('freebase.settings')
        del sys.modules['freebase.settings']
    if 'freebase.music' in sys.modules:
        #delete_module('freebase.music')
        del sys.modules['freebase.music']
    if 'freebase.dsl' in sys.modules:
        #delete_module('freebase.dsl')
        del sys.modules['freebase.dsl']
    if 'freebase.movies' in sys.modules:
        #delete_module('freebase.movies')
        del sys.modules['freebase.movies']
    if 'freebase.writers' in sys.modules:
        #delete_module('freebase.writers')
        del sys.modules['freebase.writers']

    """dbpedia"""

    if 'dbpedia' in sys.modules:
        #delete_module('dbpedia')
        del sys.modules['dbpedia']
    if 'dbpedia.basic' in sys.modules:
        #delete_module('dbpedia.basic')
        del sys.modules['dbpedia.basic']
    if 'dbpedia.country' in sys.modules:
        #delete_module('dbpedia.country')
        del sys.modules['dbpedia.country']
    if 'dbpedia.tvshows' in sys.modules:
        #delete_module('dbpedia.tvshows')
        del sys.modules['dbpedia.tvshows']
    if 'dbpedia.people' in sys.modules:
        #delete_module('dbpedia.people')
        del sys.modules['dbpedia.people']
    if 'dbpedia.settings' in sys.modules:
        #delete_module('dbpedia.settings')
        del sys.modules['dbpedia.settings']
    if 'dbpedia.music' in sys.modules:
        #delete_module('dbpedia.music')
        del sys.modules['dbpedia.music']
    if 'dbpedia.dsl' in sys.modules:
        #delete_module('dbpedia.dsl')
        del sys.modules['dbpedia.dsl']
    if 'dbpedia.movies' in sys.modules:
        #delete_module('dbpedia.movies')
        del sys.modules['dbpedia.movies']
    if 'dbpedia.writers' in sys.modules:
        #delete_module('dbpedia.writers')
        del sys.modules['dbpedia.writers']

    print sys.modules

    module_paths = {
        u"settings": u"{0}.settings",
        u"parsing": u"{0}",
    }
    modules = {}

    for module_name, module_path in module_paths.iteritems():
        try:
            modules[module_name] = import_module(module_path.format(app_name))
        except ImportError, error:
            message = u"Error importing {0!r}: {1}"
            raise ImportError(message.format(module_name, error))
    print modules
    return QuepyApp(**modules)

def delete_module(modname, paranoid=None):
    from sys import modules
    try:
        thismod = modules[modname]
    except KeyError:
        raise ValueError(modname)
    these_symbols = dir(thismod)
    if paranoid:
        try:
            paranoid[:]  # sequence support
        except:
            raise ValueError('must supply a finite list for paranoid')
        else:
            these_symbols = paranoid[:]
    del modules[modname]
    for mod in modules.values():
        try:
            delattr(mod, modname)
        except AttributeError:
            pass
        if paranoid:
            for symbol in these_symbols:
                if symbol[:2] == '__':  # ignore special symbols
                    continue
                try:
                    delattr(mod, symbol)
                except AttributeError:
                    pass

def question_sanitize(question):
    question = question.replace("'", "\'")
    question = question.replace("\"", "\\\"")
    return question


class QuepyApp(object):
    """
    Provides the quepy application API.
    """

    def __init__(self, parsing, settings):
        """
        Creates the application based on `parsing`, `settings` modules.
        """

        assert isinstance(parsing, ModuleType)
        assert isinstance(settings, ModuleType)

        self._parsing_module = parsing
        self._settings_module = settings

        # Save the settings right after loading settings module
        self._save_settings_values()

        self.tagger = get_tagger()
        self.language = getattr(self._settings_module, "LANGUAGE", None)
        if not self.language:
            raise ValueError("Missing configuration for language")

        self.rules = []
        for element in dir(self._parsing_module):
            element = getattr(self._parsing_module, element)

            try:
                if issubclass(element, QuestionTemplate) and \
                        element is not QuestionTemplate:

                    self.rules.append(element())
            except TypeError:
                continue

        self.rules.sort(key=lambda x: x.weight, reverse=True)

    def get_query(self, question):
        """
        Given `question` in natural language, it returns
        three things:

        - the target of the query in string format
        - the query
        - metadata given by the regex programmer (defaults to None)

        The query returned corresponds to the first regex that matches in
        weight order.
        """

        question = question_sanitize(question)
        for target, query, userdata in self.get_merged_queries(question):
            return target, query, userdata
        return None, None, None

    def get_queries(self, question):
        """
        Given `question` in natural language, it returns
        three things:

        - the target of the query in string format
        - the query
        - metadata given by the regex programmer (defaults to None)

        The queries returned corresponds to the regexes that match in
        weight order.
        """
        question = encoding_flexible_conversion(question)
        for expression, userdata in self._iter_compiled_forms(question):
            target, query = generation.get_code(expression, self.language)
            message = u"Interpretation {1}: {0}"
            print message.format(str(expression),
                         expression.rule_used)
            logger.debug(u"Query generated: {0}".format(query))
            yield target, query, userdata

    def _iter_compiled_forms(self, question):
        """
        Returns all the compiled form of the question.
        """

        try:
            words = list(self.tagger(question))
        except TaggingError:
            logger.warning(u"Can't parse tagger's output for: '%s'",
                           question)
            return

        logger.debug(u"Tagged question:\n" +
                     u"\n".join(u"\t{}".format(w for w in words)))

        for rule in self.rules:
            expression, userdata = rule.get_interpretation(words)
            if expression:
                yield expression, userdata

    def _save_settings_values(self):
        """
        Persists the settings values of the app to the settings module
        so it can be accesible from another part of the software.
        """

        for key in dir(self._settings_module):
            if key.upper() == key:
                value = getattr(self._settings_module, key)
                if isinstance(value, str):
                    value = encoding_flexible_conversion(value)
                setattr(settings, key, value)


    #Added


    def get_merged_queries(self, question):
        """
        Given `question` in natural language, it returns
        three things:

        - the target of the query in string format
        - the query
        - metadata given by the regex programmer (defaults to None)

        The queries returned corresponds to the regexes that match in
        weight order.
        """
        question = encoding_flexible_conversion(question)
        expr = Expression()
        for expression, userdata in self._iter_compiled_forms(question):
            expr += expression
            expr.rule_used = expression.rule_used

        target, query = generation.get_code(expr, self.language)
        message = u"Interpretation {1}: {0}"
        print message.format(str(expr),
                             expr.rule_used)
        logger.debug(u"Query generated: {0}".format(query))
        yield target, query, userdata