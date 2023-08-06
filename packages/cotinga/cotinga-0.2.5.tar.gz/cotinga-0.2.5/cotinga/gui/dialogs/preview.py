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
    gi.require_version('EvinceView', '3.0')
    gi.require_version('EvinceDocument', '3.0')
except ValueError:
    raise
else:
    from gi.repository import Gtk, EvinceDocument, EvinceView

from cotinga.core.env import REPORT_FILE
from cotinga.core.env import ICON_THEME
from cotinga.core.tools import file_uri
from cotinga.core.report import splitname
from cotinga.gui.core import IconsThemable

# Positive integers are reserved for application defined responses
PREVIOUS_PAGE = 0
NEXT_PAGE = 1


__all__ = ['PreviewDialog']


class __MetaDialog(type(Gtk.Dialog), type(IconsThemable)):
    pass


class PreviewDialog(Gtk.Dialog, IconsThemable, metaclass=__MetaDialog):

    def __init__(self, title, pages_nb, tr, parentw):
        self.tr = tr
        self.pages_nb = pages_nb
        self._current_page_nb = 0
        Gtk.Dialog.__init__(self, title, parentw, 0)
        self.set_modal(True)

        self.previous_page = Gtk.ToolButton.new()
        self.next_page = Gtk.ToolButton.new()
        self.setup_buttons_icons(ICON_THEME)

        self.add_action_widget(self.previous_page, PREVIOUS_PAGE)
        self.previous_page.connect('clicked', self.on_previous_clicked)
        self.add_action_widget(self.next_page, NEXT_PAGE)
        self.next_page.connect('clicked', self.on_next_clicked)

        self.add_buttons(Gtk.STOCK_CLOSE, Gtk.ResponseType.CLOSE,
                         Gtk.STOCK_SAVE_AS, Gtk.ResponseType.YES,
                         Gtk.STOCK_PRINT, Gtk.ResponseType.OK)

        # Prevent PreviewDialog from emitting response when next or previous
        # page buttons have been clicked
        self.connect('response', self._filter_response)

        self.set_size_request(480, 480)
        self.box = self.get_content_area()

        scroll = Gtk.ScrolledWindow()
        EvinceDocument.init()
        self.view = EvinceView.View()
        self.models = []
        for i in range(self.pages_nb):
            doc = EvinceDocument.Document.factory_get_document(
                file_uri(splitname(REPORT_FILE, i)))
            m = EvinceView.DocumentModel()
            m.set_document(doc)
            self.models.append(m)
        self.view.set_model(self.models[self.current_page_nb])
        scroll.add(self.view)
        scroll.set_hexpand(True)
        scroll.set_vexpand(True)

        self.box.add(scroll)

        self.set_navigation_buttons_sensitivity()
        self.show_all()

    def buttons_icons(self):
        """Defines icon names and fallback to standard icon name."""
        # Last item of each list is the fallback, hence must be standard
        buttons = {'previous_page': ['go-previous'],
                   'next_page': ['go-next']}
        return buttons

    def buttons_labels(self):
        """Define labels of buttons."""
        buttons = {'previous_page': self.tr('Previous'),
                   'next_page': self.tr('Next')}
        return buttons

    def _filter_response(self, widget, response_id):
        if response_id in [PREVIOUS_PAGE, NEXT_PAGE]:
            widget.stop_emission_by_name('response')

    def set_navigation_buttons_sensitivity(self):
        if self.pages_nb == 1:
            self.previous_page.set_sensitive(False)
            self.next_page.set_sensitive(False)
        elif self.current_page_nb == 0:
            self.previous_page.set_sensitive(False)
            self.next_page.set_sensitive(True)
        elif self.current_page_nb == self.pages_nb - 1:
            self.previous_page.set_sensitive(True)
            self.next_page.set_sensitive(False)
        else:
            self.previous_page.set_sensitive(True)
            self.next_page.set_sensitive(True)

    @property
    def current_page_nb(self):
        return self._current_page_nb

    @current_page_nb.setter
    def current_page_nb(self, value):
        self._current_page_nb = value
        self.set_navigation_buttons_sensitivity()
        self.view.set_model(self.models[self.current_page_nb])

    def on_previous_clicked(self, *args):
        self.current_page_nb -= 1

    def on_next_clicked(self, *args):
        self.current_page_nb += 1
