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

from abc import ABC, abstractmethod

import gi
try:
    gi.require_version('Gtk', '3.0')
except ValueError:
    raise
else:
    from gi.repository import Gtk

from .sharee import Sharee

__all__ = ['ClassesStacked']


class ClassesStacked(Sharee, ABC):

    def __init__(self, db, status, prefs, recollections, view_btns=True):
        Sharee.__init__(self, db, status, prefs, recollections)
        self.classes_stack = None
        self.stack_switcher = None
        self.view_btns = view_btns
        self.view_cols_buttons = None
        self.view_id_btn = None
        self.view_incl_btn = None
        self.view_ilevel_btn = None

    @property
    @abstractmethod
    def main_grid(self):
        """Get the object's main grid"""

    @main_grid.setter
    @abstractmethod
    def main_grid(self, value):
        """Set the object's main grid"""

    def new_switch_and_stack(self):
        if self.classes_stack:
            self.classes_stack.destroy()
        self.classes_stack = Gtk.Stack()
        self.classes_stack.set_transition_type(Gtk.StackTransitionType.NONE)
        self.classes_stack.set_transition_duration(300)
        if self.stack_switcher:
            self.stack_switcher.destroy()
        self.stack_switcher = Gtk.StackSwitcher()
        self.stack_switcher.props.margin_bottom = 10
        self.stack_switcher.props.margin_top = 10
        self.stack_switcher.set_stack(self.classes_stack)
        self.main_grid.attach(self.stack_switcher, 0, 0, 1, 1)

        if self.view_btns:
            self.view_cols_buttons = Gtk.Grid()
            self.view_cols_buttons.set_vexpand(False)
            self.view_cols_buttons.set_halign(Gtk.Align.END)
            self.view_cols_buttons.set_valign(Gtk.Align.END)
            self.view_cols_buttons.props.margin_right = 3
            view_cols_label = Gtk.Label(self.tr('View columns:'))
            view_cols_label.props.margin_right = 10
            self.view_cols_buttons.attach(view_cols_label, 0, 0, 1, 1)

            self.view_id_btn = Gtk.CheckButton('id')
            self.view_id_btn.set_active(self.status.show_col_id)
            self.view_id_btn.connect('toggled', self.on_view_id_toggled)

            self.view_incl_btn = Gtk.CheckButton(self.tr('Included'))
            self.view_incl_btn.set_active(self.status.show_col_incl)
            self.view_incl_btn.connect('toggled', self.on_view_incl_toggled)

            self.view_ilevel_btn = Gtk.CheckButton(self.tr('Initial level'))
            self.view_ilevel_btn.set_active(self.status.show_col_ilevel)
            self.view_ilevel_btn.connect('toggled',
                                         self.on_view_ilevel_toggled)

            if self.prefs.enable_devtools:
                items = [view_cols_label, self.view_id_btn, self.view_incl_btn,
                         self.view_ilevel_btn]
            else:
                items = [view_cols_label, self.view_incl_btn,
                         self.view_ilevel_btn]
            for i, item in enumerate(items):
                if i:
                    self.view_cols_buttons.attach_next_to(
                        item, items[i - 1], Gtk.PositionType.RIGHT, 1, 1)

            self.main_grid.attach_next_to(
                self.view_cols_buttons, self.stack_switcher,
                Gtk.PositionType.BOTTOM, 1, 1)

        self.main_grid.attach_next_to(self.classes_stack, self.stack_switcher,
                                      Gtk.PositionType.BOTTOM, 1, 1)

    def on_view_id_toggled(self, *args):
        pass

    def on_view_incl_toggled(self, *args):
        pass

    def on_view_ilevel_toggled(self, *args):
        pass
