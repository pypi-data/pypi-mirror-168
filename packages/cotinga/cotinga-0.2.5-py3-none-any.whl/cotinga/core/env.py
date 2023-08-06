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
from pathlib import Path

import gi
try:
    gi.require_version('Gtk', '3.0')
except ValueError:
    raise
else:
    from gi.repository import Gtk

import toml

ROOTDIR = Path(__file__).parent.parent
LOCALEDIR = ROOTDIR / 'data/locale'
GUIDIR = ROOTDIR / 'gui'
FLAGSDIR = ROOTDIR / 'data/flags'
COTINGA_ICON = str(ROOTDIR / 'data/icons/cotinga.svg')
COTINGA_FADED_ICON = str(ROOTDIR / 'data/icons/cotinga_faded.svg')
TESTDIR_DATA = Path(__file__).parent.parent.parent / 'tests/data'

pp_path = Path(__file__).parent.parent.parent / 'pyproject.toml'
if not pp_path.is_file():
    pp_path = Path(__file__).parent.parent / 'data/pyproject.toml'

with open(pp_path, 'r') as f:
    pp = toml.load(f)

__myname__ = pp['tool']['poetry']['name']
__authors__ = pp['tool']['poetry']['authors']
VERSION = pp['tool']['poetry']['version']

USER_RUN_DIR = Path.home() / '.local/share/cotinga/run'
if not USER_RUN_DIR.is_dir():
    USER_RUN_DIR.mkdir(parents=True, exist_ok=True)
RUNDOC_DIR = USER_RUN_DIR / 'doc'
if not RUNDOC_DIR.is_dir():
    RUNDOC_DIR.mkdir(parents=True, exist_ok=True)

DB_FILENAME = 'pupils.db'
DB_MIMETYPE = ['application/x-sqlite3', 'application/vnd.sqlite3']
RUNDOC_DB_URI = 'sqlite:///{}'.format(str(RUNDOC_DIR / DB_FILENAME))
RUNDOC_DB = RUNDOC_DIR / DB_FILENAME

DOCSETUP_FILENAME = 'setup.json'
DOCSETUP_MIMETYPE = ['application/json', 'text/plain']
RUN_DOCSETUP = RUNDOC_DIR / DOCSETUP_FILENAME

RECOLLECTIONS_FILENAME = 'recollections.json'
RECOLLECTIONS_MIMETYPE = ['application/json', 'text/plain']
RUNDOC_RECOLLECTIONS = RUNDOC_DIR / RECOLLECTIONS_FILENAME
DEFAULT_RECOLLECTIONS = ROOTDIR / 'data/default' / RECOLLECTIONS_FILENAME

EXTRACTED_DB = USER_RUN_DIR / DB_FILENAME
EXTRACTED_DOCSETUP = USER_RUN_DIR / DOCSETUP_FILENAME
EXTRACTED_RECOLL = USER_RUN_DIR / RECOLLECTIONS_FILENAME

USER_CONFIG_DIR = Path.home() / '.config'
USER_CONFIG_COTINGA_DIR = USER_CONFIG_DIR / __myname__
USER_CONFIG_FILE = USER_CONFIG_COTINGA_DIR / 'prefs.json'
DEFAULT_CONFIG_FILE = ROOTDIR / 'data/default/prefs.json'

STATUS = USER_RUN_DIR / 'status.json'
DEFAULT_STATUS = ROOTDIR / 'data/default/status.json'

REPORT_FILE = USER_RUN_DIR / 'report.pdf'

BELTS_JSON = USER_RUN_DIR / 'mc_belts.json'

L10N_DOMAIN = __myname__
LOCALES = \
    {'en_US': 'en-US' if sys.platform.startswith('win') else 'en_US.UTF-8',
     'fr_FR': 'fr-FR' if sys.platform.startswith('win') else 'fr_FR.UTF-8'}
SUPPORTED_LANGUAGES = list(LOCALES.keys())

DEFAULT_DOCSETUP = {lang: ROOTDIR / f'data/default/doc_setup/{lang}.json'
                    for lang in SUPPORTED_LANGUAGES}

ICON_THEME = Gtk.IconTheme.get_default()


def get_theme_name():
    return Gtk.Settings.get_default().props.gtk_theme_name


def get_icon_theme_name():
    return Gtk.Settings.get_default().props.gtk_icon_theme_name


def get_theme_provider(name=None):
    if name is None:
        name = get_theme_name()
    return Gtk.CssProvider.get_named(name, None)


THEME_STYLE_CONTEXT = Gtk.StyleContext.new()


def get_theme_colors():
    THEME_STYLE_CONTEXT.add_provider(get_theme_provider(),
                                     Gtk.STYLE_PROVIDER_PRIORITY_FALLBACK)
    _, fg_color = THEME_STYLE_CONTEXT.lookup_color('fg_color')
    _, bg_color = THEME_STYLE_CONTEXT.lookup_color('bg_color')
    _, sel_fg_color = THEME_STYLE_CONTEXT.lookup_color('selected_fg_color')
    _, sel_bg_color = THEME_STYLE_CONTEXT.lookup_color('selected_bg_color')

    return (fg_color, bg_color, sel_fg_color, sel_bg_color)


def convert_gdk_rgba_to_hex(color):
    """
    Converts Gdk.RGBA to hexadecimal value.

    :param color: the Gdk.RGBA object to convert
    :type color: gi.overrides.Gdk.RGBA
    """
    return '#{}{}{}{}'\
        .format(hex(int(255 * color.red)).replace('0x', ''),
                hex(int(255 * color.green)).replace('0x', ''),
                hex(int(255 * color.blue)).replace('0x', ''),
                hex(int(255 * color.alpha)).replace('0x', ''))
