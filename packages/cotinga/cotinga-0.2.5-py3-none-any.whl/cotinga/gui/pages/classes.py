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
from .panels import ClassesPanel


class __MetaStackedGrid(type(Gtk.Grid), type(ClassesStacked)):
    pass


class ClassesManagerPage(Gtk.Grid, ClassesStacked,
                         metaclass=__MetaStackedGrid):

    def __init__(self, db, status, prefs, recollections, parentw, store):
        self.parentw = parentw
        self.store = store
        Gtk.Grid.__init__(self)
        ClassesStacked.__init__(self, db, status, prefs, recollections,
                                view_btns=True)
        self.set_border_width(3)

        self.classnames = None
        self.panels = {}
        self.classes_stack = None
        self.stack_switcher = None
        self._main_grid = None

        self.setup_pages()

    @property
    def main_grid(self):
        return self._main_grid

    @main_grid.setter
    def main_grid(self, value):
        self._main_grid = value

    def setup_pages(self):
        if self.main_grid is not None:
            self.main_grid.destroy()
        self.main_grid = Gtk.Grid()
        self.add(self.main_grid)
        classnames = doc_setup.load()['classes']
        self.panels = {}
        self.classnames = classnames
        self.new_switch_and_stack()
        for label in classnames:
            panel = ClassesPanel(self.db, self.status, self.prefs,
                                 self.recollections, self.parentw, label,
                                 self.store)
            self.classes_stack.add_titled(panel, label, label)
            self.panels[label] = panel

        self.show_all()

    def on_view_id_toggled(self, *args):
        self.status.show_col_id = not self.status.show_col_id
        self.refresh_visible_cols()

    def on_view_incl_toggled(self, *args):
        self.status.show_col_incl = not self.status.show_col_incl
        self.refresh_visible_cols()

    def on_view_ilevel_toggled(self, *args):
        self.status.show_col_ilevel = not self.status.show_col_ilevel
        self.refresh_visible_cols()

    def refresh_visible_cols(self, *args):
        panels = [self.panels[p] for p in self.panels]
        for p in panels:
            p.col_id.set_visible(self.status.show_col_id
                                 and self.prefs.enable_devtools)
            p.col_incl.set_visible(self.status.show_col_incl)
            p.col_ilevel.set_visible(self.status.show_col_ilevel)
