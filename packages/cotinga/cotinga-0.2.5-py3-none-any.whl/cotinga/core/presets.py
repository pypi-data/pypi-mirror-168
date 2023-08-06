# -*- coding: utf-8 -*-

# Cotinga helps maths teachers creating worksheets
# and managing pupils' progression.
# Copyright 2018-2022 Nicolas Hainaux <nh.techn@gmail.com>

# This file is part of Cotinga.

# Cotinga is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.

# Cotinga is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Cotinga; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from gettext import translation

from cotinga.core import prefs
from cotinga.core.env import LOCALEDIR, L10N_DOMAIN


def TEMPLATE_PREFIX():
    tr = translation(L10N_DOMAIN, LOCALEDIR,
                     [prefs.load()['language']]).gettext
    return tr('TEMPLATE_')


def default_tests_title():
    tr = translation(L10N_DOMAIN, LOCALEDIR,
                     [prefs.load()['language']]).gettext
    return tr('Admission to <BELT>')


def GRADES_SCALES():
    tr = translation(L10N_DOMAIN, LOCALEDIR,
                     [prefs.load()['language']]).gettext
    return \
        {'ABCDE': ('A, B, C, D, E', ['A', 'B', 'C', 'D', 'E']),
         'ABCDF': (tr('A, B, C, D, F (US style)'), ['A', 'B', 'C', 'D', 'F']),
         'ABCDE_signed': (tr('A, B, C, D, E with signs'),
                          ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-',
                           'D+', 'D', 'D-', 'E+', 'E']),
         'ABCDF_signed': (tr('A, B, C, D, F with signs (US style)'),
                          ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-',
                           'D+', 'D', 'D-', 'F'])
         }


def LEVELS_SCALES():
    tr = translation(L10N_DOMAIN, LOCALEDIR,
                     [prefs.load()['language']]).gettext
    return \
        {'karate': (tr('Karate-like (7 belts: white, yellow, ...)'),
                    [tr('White belt'), tr('Yellow belt'), tr('Orange belt'),
                     tr('Green belt'), tr('Blue belt'), tr('Brown belt'),
                     tr('Black belt')]),
         'judo': (tr('Judo-like (12 belts: white, white & yellow, ...)'),
                  [tr('White belt'), tr('White and yellow belt'),
                   tr('Yellow belt'), tr('Yellow and orange belt'),
                   tr('Orange belt'), tr('Orange and green belt'),
                   tr('Green belt'), tr('Blue belt'), tr('Brown belt'),
                   tr('Black belt'), tr('Red and white belt'),
                   tr('Red belt')]),
         'martial-arts-extended': (tr('Martial arts-like (22 belts: white, '
                                      'white 1st stripe, ...)'),
                                   [tr('White belt'),
                                    tr('White belt I'),
                                    tr('White belt II'),
                                    tr('Yellow belt'),
                                    tr('Yellow belt I'),
                                    tr('Yellow belt II'),
                                    tr('Orange belt'),
                                    tr('Orange belt I'),
                                    tr('Orange belt II'),
                                    tr('Green belt'),
                                    tr('Green belt I'),
                                    tr('Green belt II'),
                                    tr('Blue belt'),
                                    tr('Blue belt I'),
                                    tr('Blue belt II'),
                                    tr('Brown belt'),
                                    tr('Brown belt I'),
                                    tr('Brown belt II'),
                                    tr('Red belt'),
                                    tr('Red belt I'),
                                    tr('Red belt II'),
                                    tr('Black belt'),
                                    ])
         }
