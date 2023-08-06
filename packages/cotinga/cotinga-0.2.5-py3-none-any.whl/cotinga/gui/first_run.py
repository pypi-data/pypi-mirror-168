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
import locale
from gettext import translation

import gi
try:
    gi.require_version('Gtk', '3.0')
except ValueError:
    raise
else:
    from gi.repository import Gtk

from microlib import XDict

from cotinga.core.env import L10N_DOMAIN, LOCALEDIR, SUPPORTED_LANGUAGES
from cotinga.core.env import DEFAULT_CONFIG_FILE


__all__ = ['setup_prefs']


def setup_prefs():
    """Run when no ~/.config/cotinga/prefs.json is found at start."""
    preferences = XDict()
    try:
        language = locale.getdefaultlocale()[0]
        assert language in SUPPORTED_LANGUAGES
    except Exception:
        # We just want to guess the default locale, and check it
        # belongs to supported languages, so for any Exception
        # raised, we fall back to the default 'en_US' country code
        language = 'en_US'
    tr = translation(L10N_DOMAIN, LOCALEDIR, [language]).gettext
    from .dialogs import PreferencesDialog
    pref_dialog = PreferencesDialog(
        tr('Cotinga - Preferences'), language, tr, None, first_run=True,
        parentw=Gtk.Window())
    pref_dialog.run()
    chosen_language = pref_dialog.chosen_language \
        if pref_dialog.chosen_language is not None \
        else language
    preferences.recursive_update(
        json.loads(DEFAULT_CONFIG_FILE.read_text()))
    preferences.recursive_update({'language': chosen_language})
    pref_dialog.destroy()
    return preferences
