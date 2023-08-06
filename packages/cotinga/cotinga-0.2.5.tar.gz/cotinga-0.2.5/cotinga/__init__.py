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

from cotinga.core.env import VERSION, USER_CONFIG_FILE
from cotinga.core import prefs, Status, Prefs, Recollections, DataBase
from cotinga.gui import first_run
from .application import Application

__version__ = VERSION


def run():
    status = Status()
    recollections = Recollections()
    if not USER_CONFIG_FILE.is_file():
        prefs.setup_default()
        prefs.save(first_run.setup_prefs())
    preferences = Prefs()
    db = DataBase()
    if status.document_loaded:
        db.load_session()
    app = Application(db, status, preferences, recollections)
    app.run()


__all__ = [run]
