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

import sys
import json
from shutil import copyfile

from microlib import XDict

from . import io
from .env import USER_CONFIG_FILE
from .env import USER_CONFIG_DIR, USER_CONFIG_COTINGA_DIR
from .env import DEFAULT_CONFIG_FILE

if sys.platform.startswith('win'):
    import ctypes
    FILE_ATTRIBUTE_HIDDEN = 0x02


def setup_default():
    if not USER_CONFIG_DIR.is_dir():
        USER_CONFIG_DIR.mkdir(parents=True)
        if sys.platform.startswith('win'):
            ctypes.windll.kernel32.SetFileAttributesW(USER_CONFIG_DIR,
                                                      FILE_ATTRIBUTE_HIDDEN)
    if not USER_CONFIG_COTINGA_DIR.is_dir():
        USER_CONFIG_COTINGA_DIR.mkdir(parents=True)
    copyfile(DEFAULT_CONFIG_FILE, USER_CONFIG_FILE)


def _from(filename):
    """Get preferences from existing file filename."""
    preferences = XDict()
    with open(filename) as f:
        preferences = XDict(json.load(f))
    return preferences


def save(data):
    """Save the user prefs file updated with given data."""
    io.save(data, USER_CONFIG_FILE)


def load():
    """Will load the values from the json prefs file."""
    preferences = _from(DEFAULT_CONFIG_FILE)
    preferences.recursive_update(_from(USER_CONFIG_FILE))
    return preferences


class Prefs(object):

    def __init__(self):
        loaded_prefs = load()
        self._language = loaded_prefs['language']
        self._enable_devtools = loaded_prefs['enable_devtools']
        self._show_toolbar_labels = loaded_prefs['show_toolbar_labels']
        self._show_generate_panel = loaded_prefs.get(
            'show_generate_panel', False)
        self._mm_venv = loaded_prefs.get('mm_venv', '')
        self._use_mm_venv = loaded_prefs.get('use_mm_venv', False)

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, value):
        # We don't check the value (the only calls to set_language() must check
        # it belongs to SUPPORTED_LANGUAGES).
        self._language = value
        save({'language': value})
        # LATER: do this only at first run, then let the user handle this
        # (when he'll be able to define the date_fmt value on his own, in the
        # prefs dialog)
        # save(_from(USER_PREFS_LOCALIZED_DEFAULT_FILES[value]))

    @property
    def enable_devtools(self):
        return self._enable_devtools

    @enable_devtools.setter
    def enable_devtools(self, value):
        self._enable_devtools = value
        save({'enable_devtools': value})

    @property
    def show_toolbar_labels(self):
        return self._show_toolbar_labels

    @show_toolbar_labels.setter
    def show_toolbar_labels(self, value):
        self._show_toolbar_labels = value
        save({'show_toolbar_labels': value})

    @property
    def show_generate_panel(self):
        return self._show_generate_panel

    @show_generate_panel.setter
    def show_generate_panel(self, value):
        self._show_generate_panel = value
        save({'show_generate_panel': value})

    @property
    def mm_venv(self):
        return self._mm_venv

    @mm_venv.setter
    def mm_venv(self, value):
        self._mm_venv = value
        save({'mm_venv': value})

    @property
    def use_mm_venv(self):
        return self._use_mm_venv

    @use_mm_venv.setter
    def use_mm_venv(self, value):
        self._use_mm_venv = value
        save({'use_mm_venv': value})
