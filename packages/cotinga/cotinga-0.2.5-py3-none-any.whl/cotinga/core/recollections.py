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

from pathlib import Path
from shutil import copyfile

from . import io
from .env import RUNDOC_RECOLLECTIONS, DEFAULT_RECOLLECTIONS


def load():
    """Load the values from the json recollections file."""
    if not RUNDOC_RECOLLECTIONS.is_file():
        copyfile(DEFAULT_RECOLLECTIONS, RUNDOC_RECOLLECTIONS)
    return io.load(RUNDOC_RECOLLECTIONS)


def save(data):
    """Save the status file updated with given data."""
    io.save(data, RUNDOC_RECOLLECTIONS)


class Recollections(object):

    def __init__(self):
        loaded_recollections = load()
        self._templates_paths = loaded_recollections['templates_paths']
        self._merge_orders = loaded_recollections['merge_orders']
        self._templates_dest_dir = loaded_recollections\
            .get('templates_dest_dir', str(Path.home()))
        self._mm_year = loaded_recollections.get('mm_year', '')
        self._process_belt_tag = loaded_recollections\
            .get('process_belt_tag', {})

    @property
    def templates_paths(self):
        return self._templates_paths

    @templates_paths.setter
    def templates_paths(self, data):
        classname, path = data
        self._templates_paths[classname] = path
        save({'templates_paths': self._templates_paths})

    @property
    def templates_dest_dir(self):
        return self._templates_dest_dir

    @templates_dest_dir.setter
    def templates_dest_dir(self, data):
        self._templates_dest_dir = data
        save({'templates_dest_dir': self._templates_dest_dir})

    @property
    def merge_orders(self):
        return self._merge_orders

    @merge_orders.setter
    def merge_orders(self, data):
        classname, pupils = data
        self._merge_orders[classname] = pupils
        save({'merge_orders': self._merge_orders})

    @property
    def mm_year(self):
        return self._mm_year

    @mm_year.setter
    def mm_year(self, data):
        self._mm_year = data
        save({'mm_year': self._mm_year})

    @property
    def process_belt_tag(self):
        return self._process_belt_tag

    @process_belt_tag.setter
    def process_belt_tag(self, data):
        classname, choice = data
        self._process_belt_tag[classname] = choice
        save({'process_belt_tag': self._process_belt_tag})
