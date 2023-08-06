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

from cotinga.gui.core.list_manager import ListManagerPanel
from cotinga.core.presets import GRADES_SCALES
from cotinga.core import constants

SEP = constants.INTERNAL_SEPARATOR


class LiteralGradingPanel(ListManagerPanel):

    def __init__(self, db, status, prefs, recollections, parentw, tr,
                 grading_setup):
        ListManagerPanel.__init__(self, db, status, prefs, recollections,
                                  grading_setup['literal_grades'],
                                  tr('Labels'),
                                  presets=(GRADES_SCALES(),
                                           tr('Load a preset scale'),
                                           tr('Replace current scale '
                                              'by: '),
                                           'insert-text'),
                                  parentw=parentw)

        self.current_edge = grading_setup['edge_literal']
        self.edges_store = Gtk.ListStore(str)
        self.currently_selected = 0

        self.previous_edges_nb = 0
        self.update_edges_store()

        self.combo = Gtk.ComboBox.new_with_model(self.edges_store)

        renderer = Gtk.CellRendererText()
        self.combo.pack_start(renderer, False)
        self.combo.add_attribute(renderer, 'text', 0)

        self.combo.set_active(self.currently_selected)
        self.combo.set_margin_top(7)
        self.combo.set_margin_left(10)

        combo_grid = Gtk.Grid()
        combo_label = Gtk.Label(tr('Edge:'))
        combo_label.set_margin_top(7)
        combo_grid.attach(combo_label, 0, 0, 1, 1)
        combo_grid.attach_next_to(self.combo, combo_label,
                                  Gtk.PositionType.RIGHT, 1, 1)
        self.attach_next_to(combo_grid, self.buttons_grid,
                            Gtk.PositionType.RIGHT, 1, 1)
        self.combo.connect('changed', self.on_edge_choice_changed)
        self.store.connect('row-deleted', self.on_content_reordered)
        self.connect('content-changed', self.on_content_changed)
        self.connect('content-removed', self.on_content_removed)
        self.connect('content-reloaded', self.update_edges_store)
        self.connect('content-new', self.update_edges_store)

    def on_content_reordered(self, *args):
        if self.detect_deletion_as_reordering:
            # print(f'[on_content_reordered] args={args}')
            rows = [row for row in self.store]
            if len(rows) >= 2:
                if rows[-1][0] == self.current_edge:
                    # the selected edge is now at the last position, hence
                    # cannot remain selected any longer; we replace it by the
                    # edge before
                    self.current_edge = rows[-2][0]
            self.update_edges_store()

    def on_content_removed(self, widget, removed_values):
        removed_values = removed_values.split(SEP)
        # print(f'[on_content_removed] removed_values={removed_values}')
        self.rebuild_edges_store()
        if self.current_edge in removed_values:
            self.currently_selected = min(len(self.edges_store) - 1,
                                          self.currently_selected)
        else:
            self.currently_selected = self.fetch_selected_edge_rank()
        self.combo.set_active(self.currently_selected)

    def on_content_changed(self, widget, old_text, new_text, *args):
        # print(f'[on_content_changed] old_text={old_text};
        # new_text={new_text}')
        for grade in self.edges_store:
            if grade[0] == old_text:
                grade[0] = new_text
                if self.current_edge == old_text:
                    self.current_edge = new_text

    def rebuild_edges_store(self):
        self.previous_edges_nb = len(self.edges_store)
        self.edges_store.clear()
        entries = [row[0] for row in self.store][:-1]
        for entry in entries:
            self.edges_store.append([entry])

    def fetch_selected_edge_rank(self):
        selected = None
        for i, edge in enumerate(row[0] for row in self.edges_store):
            if edge == self.current_edge:
                selected = i
        if selected is None:
            selected = round(self.currently_selected * len(self.edges_store)
                             / self.previous_edges_nb)
        return int(selected)

    def update_edges_store(self, *args):
        self.rebuild_edges_store()
        self.currently_selected = self.fetch_selected_edge_rank()
        if hasattr(self, 'combo'):  # this update may be called too early
            self.combo.set_active(self.currently_selected)

    def on_edge_choice_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            self.current_edge = model[tree_iter][0]
            entries = [row[0] for row in self.edges_store]
            new_selection = None
            for i, edge in enumerate(entries):
                if edge == self.current_edge:
                    new_selection = i
            if new_selection is not None:
                self.currently_selected = new_selection
