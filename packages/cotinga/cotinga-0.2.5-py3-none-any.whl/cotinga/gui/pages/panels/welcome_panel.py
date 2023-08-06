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
    from gi.repository import Gtk, GdkPixbuf

from cotinga.core.env import COTINGA_FADED_ICON
from cotinga.core.env import VERSION


class WelcomePanel(Gtk.Grid):

    def __init__(self, tr):
        Gtk.Grid.__init__(self)
        cot_icon = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            COTINGA_FADED_ICON, 192, -1, True)
        cot_icon = Gtk.Image.new_from_pixbuf(cot_icon)
        # TODO: write the welcome line bigger and bold (Pango)
        welcome_label = Gtk.Label(tr('Welcome in Cotinga'))
        # TODO: write the version line smaller and faded (Pango)
        version_label = Gtk.Label(tr('Version {}').format(VERSION))
        version_label.props.margin_bottom = 15
        # icon1 = Gtk.Image.new_from_icon_name('document-new',
        #                                      Gtk.IconSize.DIALOG)
        # icon1.props.margin = 10
        # icon2 = Gtk.Image.new_from_icon_name('document-open',
        #                                      Gtk.IconSize.DIALOG)
        # icon2.props.margin = 10
        # label = Gtk.Label(tr('You can create a new document\nor '
        #                      'load an existing one.'))

        self.set_vexpand(True)
        self.set_hexpand(True)
        self.set_halign(Gtk.Align.CENTER)
        self.set_valign(Gtk.Align.CENTER)
        self.attach(cot_icon, 0, 0, 3, 1)
        self.attach_next_to(welcome_label, cot_icon,
                            Gtk.PositionType.BOTTOM, 3, 1)
        self.attach_next_to(version_label, welcome_label,
                            Gtk.PositionType.BOTTOM, 3, 1)
        # self.attach_next_to(icon1, version_label,
        #                     Gtk.PositionType.BOTTOM, 1, 1)
        # self.attach_next_to(icon2, icon1,
        #                     Gtk.PositionType.RIGHT, 1, 1)
        # self.attach_next_to(label, icon2,
        #                     Gtk.PositionType.RIGHT, 1, 1)
        # self.show_all()
