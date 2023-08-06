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

import gi
try:
    gi.require_version('Gtk', '3.0')
    gi.require_version('GdkPixbuf', '2.0')
except ValueError:
    raise
else:
    from gi.repository import Gtk

from cotinga.core import doc_setup
from cotinga.gui.core import ClassesStacked
from .panels import MergePanel


class __MetaStackedGrid(type(Gtk.Grid), type(ClassesStacked)):
    pass


class MergePage(Gtk.Grid, ClassesStacked, metaclass=__MetaStackedGrid):

    def __init__(self, db, status, prefs, recollections, parentw):
        self.parentw = parentw
        Gtk.Grid.__init__(self)
        ClassesStacked.__init__(self, db, status, prefs, recollections,
                                view_btns=False)
        self.set_border_width(3)

        self.classnames = None
        self._main_grid = None
        self.setup_stack_and_pages()
        self.show_all()

    @property
    def main_grid(self):
        return self._main_grid

    @main_grid.setter
    def main_grid(self, value):
        self._main_grid = value

    def setup_stack_and_pages(self):
        if self.main_grid is not None:
            self.main_grid.destroy()
        self.main_grid = Gtk.Grid()
        self.add(self.main_grid)
        classnames = doc_setup.load()['classes']
        self.panels = {}
        self.classnames = classnames
        self.new_switch_and_stack()
        for label in classnames:
            panel = MergePanel(self.db, self.status, self.prefs,
                               self.recollections, self.parentw, label)
            self.classes_stack.add_titled(panel, label, label)
            self.panels[label] = panel
        self.show_all()
