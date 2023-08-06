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
from cotinga.gui.core import Sharee
from .numeric_grading_panel import NumericGradingPanel, STEPS
from .literal_grading_panel import LiteralGradingPanel


class GradingManager(Gtk.Grid, Sharee):

    def __init__(self, db, status, prefs, recollections, parentw):
        Gtk.Grid.__init__(self)
        Sharee.__init__(self, db, status, prefs, recollections)
        self.set_border_width(10)
        self.set_vexpand(True)
        self.set_hexpand(True)

        grading_setup = doc_setup.load()['grading']

        self.numeric_panel = NumericGradingPanel(grading_setup)
        self.literal_panel = LiteralGradingPanel(db, status, prefs,
                                                 recollections, parentw,
                                                 self.tr,
                                                 grading_setup)
        self.numeric_panel.show()
        self.literal_panel.show()

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(
            Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(300)

        self.stack.add_titled(self.numeric_panel, 'numeric',
                              self.tr('Numeric'))
        self.stack.add_titled(self.literal_panel, 'literal',
                              self.tr('Literal'))

        self.stack.set_visible_child_name(grading_setup['choice'])

        self.stack_switcher = Gtk.StackSwitcher()
        self.stack_switcher.props.margin_bottom = 10
        self.stack_switcher.set_stack(self.stack)
        self.attach(self.stack_switcher, 0, 0, 1, 1)
        self.attach_next_to(self.stack, self.stack_switcher,
                            Gtk.PositionType.BOTTOM, 1, 1)
        self.show_all()

    def get_grading(self):
        step = list(STEPS.keys())[list(STEPS.values())
                                  .index(str(self.numeric_panel.step))]
        return {'choice': self.stack.get_visible_child_name(),
                'step': step,
                'minimum': self.numeric_panel.minimum,
                'maximum': self.numeric_panel.maximum,
                'edge_numeric': self.numeric_panel.edge,
                'literal_grades': [row[0]
                                   for row in self.literal_panel.store
                                   if row[0] is not None],
                'edge_literal': self.literal_panel.current_edge}
