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
    from gi.repository import Gtk, GObject

from cotinga.gui.core import IconsThemable, Sharee
from cotinga.core.errors import FileError
from cotinga.core.env import ICON_THEME
from cotinga.core import doc_setup, document
from cotinga.core.tools import Listing, calculate_attained_level
from cotinga.models import Pupils
from .dialogs import DocSetupDialog
from .dialogs import SaveAsFileDialog, SaveBeforeDialog
from .dialogs import run_message_dialog, OpenFileDialog


class __MetaToolbar(type(Gtk.Toolbar), type(IconsThemable),
                    type(Sharee)):
    pass


class MainToolbar(Gtk.Toolbar, IconsThemable, Sharee, metaclass=__MetaToolbar):

    @GObject.Signal
    def do_refresh_app_title(self):
        """Notify the app title must be refreshed."""

    @GObject.Signal
    def do_refresh(self):
        """Notify the app must be refreshed."""

    def __init__(self, db, status, prefs, recollections, parentw):
        self.parentw = parentw
        Gtk.Toolbar.__init__(self)
        IconsThemable.__init__(self)
        Sharee.__init__(self, db, status, prefs, recollections)

        self.doc_new_button = Gtk.ToolButton.new()
        self.doc_new_button.set_vexpand(False)
        self.doc_new_button.set_halign(Gtk.Align.CENTER)
        self.doc_new_button.set_valign(Gtk.Align.CENTER)
        self.doc_new_button.connect('clicked', self.on_doc_new_clicked)
        self.add(self.doc_new_button)

        self.doc_open_button = Gtk.ToolButton.new()
        self.doc_open_button.set_vexpand(False)
        self.doc_open_button.set_halign(Gtk.Align.CENTER)
        self.doc_open_button.set_valign(Gtk.Align.CENTER)
        self.doc_open_button.connect('clicked', self.on_doc_open_clicked)
        self.add(self.doc_open_button)

        self.doc_save_button = Gtk.ToolButton.new()
        self.doc_save_button.set_vexpand(False)
        self.doc_save_button.set_halign(Gtk.Align.CENTER)
        self.doc_save_button.set_valign(Gtk.Align.CENTER)
        self.doc_save_button.connect('clicked', self.on_doc_save_clicked)
        self.add(self.doc_save_button)

        self.doc_save_as_button = Gtk.ToolButton.new()
        self.doc_save_as_button.props.icon_name = 'document-save-as'
        self.doc_save_as_button.set_vexpand(False)
        self.doc_save_as_button.set_halign(Gtk.Align.CENTER)
        self.doc_save_as_button.set_valign(Gtk.Align.CENTER)
        self.doc_save_as_button.connect('clicked', self.on_doc_save_as_clicked)
        self.add(self.doc_save_as_button)

        self.doc_close_button = Gtk.ToolButton.new()
        self.doc_close_button.set_vexpand(False)
        self.doc_close_button.set_halign(Gtk.Align.CENTER)
        self.doc_close_button.set_valign(Gtk.Align.CENTER)
        self.doc_close_button.connect('clicked', self.on_doc_close_clicked)
        self.add(self.doc_close_button)

        self.doc_setup_button = Gtk.ToolButton.new()
        self.doc_setup_button.set_vexpand(False)
        self.doc_setup_button.set_halign(Gtk.Align.CENTER)
        self.doc_setup_button.set_valign(Gtk.Align.CENTER)
        self.doc_setup_button.connect('clicked', self.on_doc_setup_clicked)
        self.add(self.doc_setup_button)

        # LATER: add a document-open-recent button

        self.buttons = {'document-new': self.doc_new_button,
                        'document-open': self.doc_open_button,
                        'document-close': self.doc_close_button,
                        'document-save': self.doc_save_button,
                        'document-save-as': self.doc_save_as_button,
                        'document-setup': self.doc_setup_button}
        self.setup_buttons_icons(ICON_THEME)
        self.refresh()

    def buttons_icons(self):
        """Define icon names and fallback to standard icon name."""
        # Last item of each list is the fallback, hence must be standard
        buttons = {'doc_new_button': ['document-new'],
                   'doc_open_button': ['document-open'],
                   'doc_save_button': ['document-save'],
                   'doc_save_as_button': ['document-save-as'],
                   'doc_close_button': ['document-close', 'window-close'],
                   'doc_setup_button': ['gnome-settings',
                                        'preferences-desktop'],
                   }
        return buttons

    def buttons_labels(self):
        """Define labels of buttons."""
        buttons = {'doc_new_button': self.tr('New'),
                   'doc_open_button': self.tr('Open'),
                   'doc_save_button': self.tr('Save'),
                   'doc_save_as_button': self.tr('Save as...'),
                   'doc_close_button': self.tr('Close'),
                   'doc_setup_button': self.tr('Settings'),
                   }
        return buttons

    def refresh(self):
        self.buttons['document-save'].set_sensitive(
            self.status.document_modified)
        self.buttons['document-save-as'].set_sensitive(
            self.status.document_loaded)
        self.buttons['document-setup'].set_sensitive(
            self.status.document_loaded)
        self.buttons['document-close'].set_sensitive(
            self.status.document_loaded)

    def save_before(self, message):
        """
        If document is modified, ask if it should be saved.

        Return True if the current action should be cancelled instead.

        :param message: a string to specify the reason of the action
        :type message: str
        :rtype: bool
        """
        cancel = False
        if self.status.document_modified:
            dialog = SaveBeforeDialog(message, self.tr, self.parentw)
            response = dialog.run()
            dialog.destroy()
            if response == Gtk.ResponseType.YES:
                cancel = self.save()
            elif response == Gtk.ResponseType.CANCEL:
                cancel = True
        return cancel

    def save(self):
        """Save the current document without changing the file name."""
        cancel = False
        if self.status.document_name == '':
            cancel = self.save_as()
        else:
            document.save_as(self.status.document_name)
            self.status.document_modified = False
            self.refresh()
            self.emit('do-refresh-app-title')
        return cancel

    def save_as(self):
        """Save the current document with a new name."""
        cancel = False
        dialog = SaveAsFileDialog(self.db, self.status, self.prefs,
                                  self.recollections, self.parentw)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            doc_name = dialog.get_filename()
            if not doc_name.endswith('.tgz'):
                doc_name += '.tgz'
            self.status.document_name = doc_name
            document.save_as(self.status.document_name)
            self.status.document_modified = False
            self.refresh()
            self.emit('do-refresh-app-title')
        elif response == Gtk.ResponseType.CANCEL:
            cancel = True
        dialog.destroy()
        return cancel

    def open_(self):
        cancel = self.save_before(
            self.tr('Save current document before opening another one?'))
        if not cancel:
            dialog = OpenFileDialog(self.tr, self.parentw)
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                doc_name = dialog.get_filename()
                try:
                    document.check_file(doc_name)
                except FileError as excinfo:
                    run_message_dialog(
                        self.tr('Cannot load file'),
                        self.tr('Cotinga cannot use this file.\n'
                                'Details: {details}')
                        .format(details=str(excinfo)),
                        'dialog-error', self.parentw)
                else:
                    terminate_session = False
                    if self.status.document_loaded:
                        terminate_session = True
                    self.status.document_loaded = False
                    document.open_(self.db, terminate_session)
                    self.status.document_modified = False
                    self.status.document_name = doc_name
                    self.status.filters = doc_setup.load()['classes']
                    self.status.document_loaded = True
                    self.emit('do-refresh')
            dialog.destroy()

    def on_doc_new_clicked(self, widget):
        """Called on "new file" clicks"""
        cancel = self.save_before(
            self.tr('Save current document before creating a new one?'))
        if not cancel:
            document.new(self.db)
            self.status.document_loaded = True
            self.status.document_modified = False
            self.status.document_name = ''
            self.status.filters = []
            self.refresh()
            self.emit('do-refresh')

    def on_doc_close_clicked(self, widget):
        """Called on "close file" clicks"""
        cancel = self.save_before(
            self.tr('Save current document before closing it?'))
        if not cancel:
            document.close(self.db)
            self.status.document_loaded = False
            self.status.document_modified = False
            self.status.document_name = ''
            self.status.filters = []
            self.refresh()
            self.emit('do-refresh')

    def on_doc_save_as_clicked(self, widget):
        """Called on "save as" clicks"""
        self.save_as()

    def on_doc_save_clicked(self, widget):
        """Called on "save as" clicks"""
        self.save()

    def on_doc_open_clicked(self, widget):
        """Called on "open file" clicks"""
        self.open_()

    def on_doc_setup_clicked(self, widget):
        """Called on "document setup" clicks"""
        dialog = DocSetupDialog(self.db, self.status, self.prefs,
                                self.recollections, self.parentw)
        dialog.set_modal(True)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            # LATER: when validating, if the user is inserting something that
            # he did not validate yet via return, then it's lost. Check if
            # there's a way to keep the entry if it's not
            # None (e.g. validate it or not via cell_edited().
            # The 'editing-canceled' event from CellRendererText seems useless
            # unfortunately (the text is then already set to None)
            # Maybe a way is to disable the validate button when insert_button
            # is clicked and until the entry is validated by return.
            new_levels = [row[0] for row in dialog.levels_panel.store
                          if row[0] is not None]
            new_special_grades = [row[0]
                                  for row in dialog.special_grades_panel.store
                                  if row[0] is not None]
            new_grading = dialog.grading_manager.get_grading()
            new_classes = [row[0]
                           for row in dialog.classes_panel.store
                           if row[0] is not None]
            docsetup = doc_setup.load()
            previous_levels = docsetup['levels']
            previous_special_grades = docsetup['special_grades']
            previous_grading = docsetup['grading']
            previous_classes = docsetup['classes']
            if new_classes != previous_classes:
                for (old, new) in dialog.classes_renamed:
                    pupils_list = self.db.session.query(Pupils).filter(
                        Pupils.classnames.contains([old])).all()
                    for p in pupils_list:
                        p.classnames = Listing([cl if cl != old else new
                                                for cl in p.classnames])
                    self.db.session.commit()
                # Remove filters of removed classes from filters ON, if any
                self.status.filters = [label
                                       for label in self.status.filters
                                       if label in new_classes]
            if new_levels != previous_levels:
                pupils_list = self.db.session.query(Pupils).all()
                for p in pupils_list:
                    p.initial_level = \
                        new_levels[previous_levels.index(p.initial_level)]
                    p.attained_level = \
                        calculate_attained_level(p.initial_level, new_levels,
                                                 new_grading, p.grades,
                                                 new_special_grades)
                self.db.session.commit()
            if any(new != previous
                   for (new, previous) in zip([new_levels,
                                               new_special_grades,
                                               new_grading,
                                               new_classes],
                                              [previous_levels,
                                               previous_special_grades,
                                               previous_grading,
                                               previous_classes])):
                docsetup = doc_setup.save(
                    {'levels': new_levels,
                     'special_grades': new_special_grades,
                     'classes': new_classes,
                     'grading': new_grading})
                self.status.document_modified = True
                self.emit('do-refresh')
        dialog.destroy()
