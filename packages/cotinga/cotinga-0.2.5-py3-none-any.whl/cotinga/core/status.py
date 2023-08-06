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

from shutil import copyfile

from . import io
from .env import STATUS, DEFAULT_STATUS


def load():
    """Load the values from the json status file."""
    if not STATUS.is_file():  # Should only happen at first run
        copyfile(DEFAULT_STATUS, STATUS)
    return io.load(STATUS)


def save(data):
    """Save the status file updated with given data."""
    io.save(data, STATUS)


class Status(object):

    def __init__(self):
        loaded_status = load()
        for key in loaded_status.keys():
            setattr(self, f'_{key}', loaded_status[key])

    @property
    def document_loaded(self):
        return self._document_loaded

    @document_loaded.setter
    def document_loaded(self, value):
        # LATER: maybe check the value is boolean
        self._document_loaded = value
        save({'document_loaded': value})

    @property
    def document_modified(self):
        return self._document_modified

    @document_modified.setter
    def document_modified(self, value):
        # LATER: maybe check the value is boolean
        self._document_modified = value
        save({'document_modified': value})

    @property
    def document_name(self):
        return self._document_name

    @document_name.setter
    def document_name(self, value):
        self._document_name = value
        save({'document_name': value})

    @property
    def filters(self):
        return self._filters

    @filters.setter
    def filters(self, value):
        self._filters = value
        save({'filters': value})

    @property
    def show_col_id(self):
        return self._show_col_id

    @show_col_id.setter
    def show_col_id(self, value):
        self._show_col_id = value
        save({'show_col_id': value})

    @property
    def show_col_incl(self):
        return self._show_col_incl

    @show_col_incl.setter
    def show_col_incl(self, value):
        self._show_col_incl = value
        save({'show_col_incl': value})

    @property
    def show_col_ilevel(self):
        return self._show_col_ilevel

    @show_col_ilevel.setter
    def show_col_ilevel(self, value):
        self._show_col_ilevel = value
        save({'show_col_ilevel': value})
