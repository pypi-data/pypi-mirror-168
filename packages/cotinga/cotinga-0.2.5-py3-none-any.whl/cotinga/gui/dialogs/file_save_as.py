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

from datetime import datetime

import gi
try:
    gi.require_version('Gtk', '3.0')
except ValueError:
    raise
else:
    from gi.repository import Gtk

from cotinga.core import doc_setup
from cotinga.gui.core import Sharee
from cotinga.core.tools import add_cot_filters, add_pdf_filters

__all__ = ['SaveAsFileDialog']


class __MetaDialog(type(Gtk.FileChooserDialog), type(Sharee)):
    pass


class SaveAsFileDialog(Gtk.FileChooserDialog, Sharee, metaclass=__MetaDialog):

    def __init__(self, db, status, prefs, recollections, parentw,
                 report=False):
        """
        :param report: whether we're about to save a report rather than the
        current user file
        :type report: bool
        """
        Sharee.__init__(self, db, status, prefs, recollections)
        Gtk.FileChooserDialog.__init__(self, self.tr('Please choose a file'),
                                       parentw,
                                       Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_SAVE_AS,
                                        Gtk.ResponseType.OK))
        if report:
            date_fmt = doc_setup.load()['report']['date_fmt']
            date = datetime.now().strftime(date_fmt).replace('/', '-')
            self.set_current_name(self.tr('Report {date}.pdf')
                                  .format(date=date))
        else:
            doc_name = status.document_name
            if doc_name == '':
                self.set_current_name(self.tr('Untitled.tgz'))
            else:
                self.set_filename(doc_name)
        self.set_modal(True)
        self.set_do_overwrite_confirmation(True)
        if report:
            add_pdf_filters(self)
        else:
            add_cot_filters(self)
