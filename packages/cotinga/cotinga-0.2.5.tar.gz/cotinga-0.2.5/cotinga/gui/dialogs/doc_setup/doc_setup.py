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
except ValueError:
    raise
else:
    from gi.repository import Gtk

from cotinga.core import doc_setup
from cotinga.models import Pupils
from cotinga.gui.core import Sharee
from cotinga.gui.core.list_manager import ListManagerPanel
from .grading_manager import GradingManager
from .classes_manager_panel import ClassesManagerPanel

__all__ = ['DocSetupDialog']


class DocSetupDialog(Gtk.Dialog, Sharee):

    def __init__(self, db, status, prefs, recollections, parentw):
        Sharee.__init__(self, db, status, prefs, recollections)
        from cotinga.core.presets import LEVELS_SCALES
        Gtk.Dialog.__init__(self, self.tr('Document setup'), parentw, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_size_request(350, 200)
        self.box = self.get_content_area()
        self.grading_manager = GradingManager(db, status, prefs, recollections,
                                              parentw)
        docsetup = doc_setup.load()
        self.levels_panel = \
            ListManagerPanel(self.db, self.status, self.prefs,
                             self.recollections,
                             docsetup['levels'], self.tr('Labels'),
                             presets=(LEVELS_SCALES(),
                                      self.tr('Load a preset scale'),
                                      self.tr('Replace current scale by: '),
                                      'document-import'),
                             parentw=parentw)
        self.special_grades_panel = \
            ListManagerPanel(self.db, self.status, self.prefs,
                             self.recollections,
                             docsetup['special_grades'], self.tr('Labels'),
                             mini_items_nb=0)
        # Classes that cannot be removed by the remove button
        locked_classes = [
            classname
            for classname in docsetup['classes']
            if len(db.session.query(Pupils)
                   .filter(Pupils.classnames.contains([classname]))
                   .all()) >= 1]
        self.classes_renamed = []
        self.classes_panel = \
            ClassesManagerPanel(self.db, self.status, self.prefs,
                                self.recollections,
                                docsetup['classes'], self.tr('Labels'),
                                mini_items_nb=0, locked=locked_classes,
                                classes_renamed=self.classes_renamed)
        # From: https://lazka.github.io/pgi-docs/Gtk-3.0/classes/
        # Notebook.html#Gtk.Notebook.set_current_page
        # "it is recommended to show child widgets before adding them to a "
        # "notebook."
        # Hence it is not recommended to add pages first and use get_children()
        # to browse pages to show them...
        for page in [self.grading_manager, self.levels_panel,
                     self.special_grades_panel, self.classes_panel]:
            page.show()
        self.notebook = Gtk.Notebook()
        self.notebook.append_page(self.classes_panel,
                                  Gtk.Label(self.tr('Classes')))
        self.notebook.append_page(self.levels_panel,
                                  Gtk.Label(self.tr('Levels')))
        self.notebook.append_page(self.grading_manager,
                                  Gtk.Label(self.tr('Grading')))
        self.notebook.append_page(self.special_grades_panel,
                                  Gtk.Label(self.tr('Special grades')))
        self.notebook.set_current_page(0)
        self.box.add(self.notebook)
        self.show_all()
        self.from_page_num = self.notebook.get_current_page()
