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

import json

from . import io
from .env import RUN_DOCSETUP, DEFAULT_DOCSETUP
from . import prefs


def load():
    """Load the complete setup of current loaded file."""
    try:
        data = io.load(RUN_DOCSETUP)
    except KeyError:
        data = dict()
    # Ensure compatibility with cotinga <= 0.2.4
    if 'title' not in data['report']:
        lang = prefs.load()['language']
        default_docsetup = json.loads(DEFAULT_DOCSETUP[lang].read_text())
        data['report']['title'] = default_docsetup['report']['title']
    if 'subtitle' not in data['report']:
        lang = prefs.load()['language']
        default_docsetup = json.loads(DEFAULT_DOCSETUP[lang].read_text())
        data['report']['subtitle'] = default_docsetup['report']['subtitle']
    return data


def save(data):
    """Save the document setup updated with given data."""
    io.save(data, RUN_DOCSETUP)
