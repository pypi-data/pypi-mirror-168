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

import time
from operator import itemgetter

import gi
try:
    gi.require_version('Gtk', '3.0')
    gi.require_version('Gdk', '3.0')
    gi.require_version('Pango', '1.0')
except ValueError:
    raise
else:
    from gi.repository import GLib, Gdk, Gtk, GObject, Pango


from cotinga.core.env import ICON_THEME, get_icon_theme_name, get_theme_colors
from cotinga.core.env import convert_gdk_rgba_to_hex
from cotinga.core.tools import Listing, calculate_attained_level
from cotinga.core.tools import build_view
from cotinga.models import Pupils, PUPILS_COL_NBS
from cotinga.gui.core.list_manager import ListManagerBase
from cotinga.gui.dialogs import ComboDialog, run_message_dialog
from cotinga.gui.dialogs import ConfirmationDialog
from cotinga.core import constants
from cotinga.core.errors import EmptyContentError, ReservedCharsError
from cotinga.gui.core import ID, INCLUDED, CLASSES, FULLNAME
from cotinga.gui.core import ILEVEL, ALEVEL, GRADES
from cotinga.gui.core import PupilsView, MetaView

SEP = constants.INTERNAL_SEPARATOR


class ClassesPanel(ListManagerBase, PupilsView, metaclass=MetaView):

    @GObject.Signal(arg_types=(str, int,))
    def grades_columns_changed(self, *args):
        """Notify that a grade column has been added or removed."""

    @GObject.Signal(arg_types=(str, str, str,))
    def pupils_list_changed(self, *args):
        """
        Notify that some pupils have been removed from or added to a class.
        """

    @GObject.Signal()
    def refresh_title_toolbar(self):
        """Notify that the title and toolbar of the app must be refreshed."""

    def __init__(self, db, status, prefs, recollections, parentw, classname,
                 store):
        # TODO: change mouse cursor when hovering editable columns
        self.classname = classname
        self.parentw = parentw
        ListManagerBase.__init__(self, db, status, prefs, recollections,
                                 setup_buttons_icons=False, mini_items_nb=0,
                                 store=store, parentw=parentw)

        # self.store.set_sort_column_id(FULLNAME, Gtk.SortType.ASCENDING)

        # Treeview and its components
        PupilsView.__init__(self)

        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.add(self.treeview)
        self.scrollable_treelist.set_vexpand(True)
        self.scrollable_treelist.set_hexpand(False)
        self.scrollable_treelist.set_propagate_natural_height(True)
        self.attach(self.scrollable_treelist, 0, 0, 2, 1)

        # TOP TOOLS (add/remove pupil)
        self.top_buttons = Gtk.Grid()

        self.insert_button.set_vexpand(False)
        self.insert_button.set_halign(Gtk.Align.CENTER)
        self.insert_button.set_valign(Gtk.Align.CENTER)
        self.insert_button.props.margin_right = 10
        self.insert_button.connect('clicked', self.on_insert_clicked)
        self.top_buttons.attach(self.insert_button, 0, 0, 1, 1)

        self.paste_pupils_button = Gtk.ToolButton.new()
        self.paste_pupils_button.set_vexpand(False)
        self.paste_pupils_button.set_hexpand(False)
        self.paste_pupils_button.set_halign(Gtk.Align.CENTER)
        self.paste_pupils_button.set_valign(Gtk.Align.CENTER)
        self.paste_pupils_button.props.margin_right = 10
        self.paste_pupils_button.connect('clicked',
                                         self.on_paste_pupils_clicked)
        self.top_buttons.attach_next_to(self.paste_pupils_button,
                                        self.insert_button,
                                        Gtk.PositionType.RIGHT, 1, 1)

        self.remove_button.set_vexpand(False)
        self.remove_button.set_halign(Gtk.Align.CENTER)
        self.remove_button.set_valign(Gtk.Align.CENTER)
        self.remove_button.set_sensitive(False)
        self.remove_button.connect('clicked', self.on_remove_clicked)
        self.top_buttons.attach_next_to(self.remove_button,
                                        self.paste_pupils_button,
                                        Gtk.PositionType.RIGHT, 1, 1)

        self.edit_level_button = Gtk.ToolButton.new()
        self.edit_level_button.set_vexpand(False)
        self.edit_level_button.set_hexpand(False)
        self.edit_level_button.set_halign(Gtk.Align.CENTER)
        self.edit_level_button.set_valign(Gtk.Align.CENTER)
        self.edit_level_button.props.margin_right = 10
        self.edit_level_button.set_sensitive(False)
        self.edit_level_button.connect('clicked',
                                       self.on_edit_level_clicked)
        self.top_buttons.attach_next_to(self.edit_level_button,
                                        self.remove_button,
                                        Gtk.PositionType.RIGHT, 1, 1)

        self.edit_class_button = Gtk.ToolButton.new()
        self.edit_class_button.set_vexpand(False)
        self.edit_class_button.set_hexpand(False)
        self.edit_class_button.set_halign(Gtk.Align.CENTER)
        self.edit_class_button.set_valign(Gtk.Align.CENTER)
        self.edit_class_button.props.margin_right = 10
        self.edit_class_button.set_sensitive(False)
        self.edit_class_button.connect('clicked',
                                       self.on_edit_class_clicked)
        self.top_buttons.attach_next_to(self.edit_class_button,
                                        self.edit_level_button,
                                        Gtk.PositionType.RIGHT, 1, 1)

        self.add_grade_button = Gtk.ToolButton.new()
        self.add_grade_button.set_vexpand(False)
        self.add_grade_button.set_margin_bottom(5)
        self.add_grade_button.connect('clicked', self.on_add_grade_clicked)

        self.paste_grades_button = Gtk.ToolButton.new()
        self.paste_grades_button.set_vexpand(False)
        self.paste_grades_button.connect('clicked',
                                         self.on_paste_grades_clicked)

        self.remove_grade_button = Gtk.ToolButton.new()
        self.remove_grade_button.set_vexpand(False)
        self.remove_grade_button.connect('clicked',
                                         self.on_remove_grade_clicked)

        pupils_nb = self.pupils_nb()
        self.paste_grades_button.set_sensitive(pupils_nb >= 1)
        self.add_grade_button.set_sensitive(pupils_nb >= 1)
        self.remove_grade_button.set_sensitive(False)

        self.top_buttons.attach_next_to(self.add_grade_button,
                                        self.edit_class_button,
                                        Gtk.PositionType.RIGHT, 1, 1)

        self.top_buttons.attach_next_to(self.paste_grades_button,
                                        self.add_grade_button,
                                        Gtk.PositionType.RIGHT, 1, 1)

        self.top_buttons.attach_next_to(self.remove_grade_button,
                                        self.paste_grades_button,
                                        Gtk.PositionType.RIGHT, 1, 1)
        self.top_tools = Gtk.Grid()
        self.top_tools.set_hexpand(False)
        self.top_tools.props.margin_bottom = 0
        self.top_tools.props.margin_top = 3
        self.top_tools.attach(self.top_buttons, 0, 0, 1, 1)

        self.attach_next_to(self.top_tools, self.scrollable_treelist,
                            Gtk.PositionType.TOP, 1, 1)

        topvoid_grid = Gtk.Grid()
        topvoid_grid.set_hexpand(True)
        self.attach_next_to(topvoid_grid, self.top_tools,
                            Gtk.PositionType.RIGHT, 1, 1)

        self.clip = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
        self.clip2 = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        # self.treeview.connect('set-focus-child', self.on_set_focus_child)
        self.started_edition = False
        self.setup_buttons_icons(ICON_THEME)

        # Only colgrades can be user selected
        self.user_selected_col = None
        self.user_selected_col_nb = None
        self.unselected_rows = None

    def visible_pupils(self):
        result = []
        for i, row in enumerate(self.store):
            if self.class_filter_func(self.store,
                                      self.store.get_iter(Gtk.TreePath(i)),
                                      None):
                result.append(row)
        return sorted(result, key=itemgetter(FULLNAME))

    def pupils_nb(self):
        return len(self.visible_pupils())

    def class_filter_func(self, model, treeiter, data):
        """Test if the class in the row is the one of the panel"""
        return any(cl.strip() == self.classname
                   for cl in model[treeiter][CLASSES].split(','))

    def _adjust_tv_columns_renderers(self):
        self.renderer_ilevel = Gtk.CellRendererCombo()
        self.renderer_incl.connect('toggled', self.on_included_toggled)

        self.renderer_name.props.editable = True
        self.renderer_name.props.editable_set = True
        self.renderer_name.connect('editing-started', self.on_editing_started)
        self.renderer_name.connect('editing-canceled',
                                   self.on_editing_canceled)
        self.renderer_name.connect('edited', self.on_name_edited)

        liststore_levels = Gtk.ListStore(str)
        for item in self.levels:
            liststore_levels.append([item])
        self.renderer_ilevel.set_property('editable', True)
        self.renderer_ilevel.set_property('model', liststore_levels)
        self.renderer_ilevel.set_property('text-column', 0)
        self.renderer_ilevel.set_property('has-entry', False)
        self.renderer_ilevel.connect('editing-started',
                                     self.on_editing_started)
        self.renderer_ilevel.connect('edited', self.on_initial_level_edited)
        self.renderer_ilevel.connect('editing-canceled',
                                     self.on_editing_canceled)

    def _adjust_tv_columns(self):
        self.col_incl.set_visible(self.status.show_col_incl)
        self.col_class.set_visible(False)
        # self.col_name.set_sort_column_id(2)
        # self.col_ilevel.set_sort_column_id(3)
        self.col_ilevel.set_visible(self.status.show_col_ilevel)
        # self.col_alevel.set_sort_column_id(4)

    def _adjust_grade_renderer(self):
        self.grade_renderer.props.editable = True
        self.grade_renderer.props.editable_set = True
        self.grade_renderer.connect('edited', self.on_grade_edited)
        self.grade_renderer.connect('editing-canceled',
                                    self.on_editing_canceled)
        self.grade_renderer.connect('editing-started', self.on_editing_started)
        self.grade_renderer.props.foreground_set = True

    @property
    def default_row_values(self):
        return [None, True, self.classname, '', self.levels[0],
                self.levels[0], Listing(None)]

    @property
    def grades_nb(self):
        class_pupils = self.db.session.query(Pupils)\
            .filter(Pupils.classnames.contains([self.classname]))\
            .all()
        return max([len(pupil.grades or []) for pupil in class_pupils] or [0])

    def buttons_icons(self):
        # Last item of each list is the fallback, hence must be standard
        buttons = {'insert_button': ['contact-new'],
                   'remove_button': ['list-remove-user', 'edit-delete'],
                   'edit_level_button': ['starred'],
                   'edit_class_button': ['go-next'],
                   'paste_pupils_button': ['user-group-new',
                                           'stock_new-meeting',
                                           'resource-group-new',
                                           'stock_people', 'edit-paste'],
                   'paste_grades_button': ['edit-paste'],
                   'remove_grade_button': ['list-remove'],
                   'add_grade_button': ['list-add']}
        if any(get_icon_theme_name().startswith(name)
               for name in ['Numix-Circle', 'Paper']):
            buttons.update({'paste_grades_button': ['view-task', 'stock_task',
                                                    'edit-paste']})
        return buttons

    def buttons_labels(self):
        """Define labels of buttons."""
        buttons = {'insert_button': self.tr('Insert a pupil'),
                   'remove_button': self.tr('Remove pupils'),
                   'edit_level_button': self.tr('Edit initial level'),
                   'edit_class_button': self.tr('Add to another class'),
                   'paste_pupils_button': self.tr('Paste pupils'),
                   'paste_grades_button': self.tr('Paste grades'),
                   'remove_grade_button': self.tr('Remove grade'),
                   'add_grade_button': self.tr('Add new grade')}
        return buttons

    def set_buttons_sensitivity(self):
        ListManagerBase.set_buttons_sensitivity(self)
        editing = self.started_insertion or self.started_edition
        rows_nb = len(self.selection.get_selected_rows()[1])
        lock_grades_btns = True
        colgrades_nb = self.treeview.get_n_columns() - GRADES
        no_colgrade_at_all = (colgrades_nb == 0)
        pupils_nb = self.pupils_nb()
        for p in self.visible_pupils():
            pupil_grades = self.store[p.path][GRADES].cols
            if (len(pupil_grades) and len(pupil_grades) == colgrades_nb
                    and pupil_grades[-1] != ''):
                lock_grades_btns = False
                break
        self.insert_button.set_sensitive(not editing and rows_nb <= 1
                                         and self.user_selected_col_nb is None)
        self.paste_pupils_button.set_sensitive(
            not editing and rows_nb <= 1 and self.user_selected_col_nb is None)
        self.paste_grades_button.set_sensitive(not editing and pupils_nb
                                               and rows_nb <= 1
                                               and (no_colgrade_at_all
                                                    or not lock_grades_btns))
        self.add_grade_button.set_sensitive(
            not editing and pupils_nb and rows_nb <= 1
            and (no_colgrade_at_all or not lock_grades_btns)
            and self.user_selected_col is None)
        self.remove_grade_button.set_sensitive(
            self.user_selected_col is not None)
        self.edit_level_button.set_sensitive(rows_nb >= 2)
        self.edit_class_button.set_sensitive(rows_nb >= 1
                                             and len(self.classes) >= 2
                                             and not editing)

    def _adjust_grades_column(self, nth):
        self._grades_columns[nth].props.max_width = 80
        self._grades_columns[nth].set_clickable(True)
        self._grades_columns[nth].connect('clicked', self.on_column_clicked)

    def on_key_release(self, widget, ev, data=None):
        if ev.keyval == Gdk.KEY_Escape:
            if self.started_insertion:
                self.cancel_insertion()
            if self.started_edition or self.started_insertion:
                self.post_edit_cleanup()
            self.set_buttons_sensitivity()
            if self.user_selected_col_nb is not None:
                self.unselect_col(self.get_selected_col())

    def on_tree_selection_changed(self, selection):
        ListManagerBase.set_buttons_sensitivity(self)
        if self.user_selected_col_nb is not None:
            self.unselect_col(self.get_selected_col())
            self.unselected_rows = None
        self.set_buttons_sensitivity()

    def on_paste_grades_clicked(self, widget):
        # TODO: factorize at least parts of this method with
        # on_paste_pupils_clicked
        text = self.clip.wait_for_text()
        if text is None:
            text = self.clip2.wait_for_text()
        if text is not None:
            if '\t' in text:
                sep = '\t'
            else:
                sep = '\n'
            lines = text.strip().split(sep)

            do_paste = True
            # LATER: (when showing data before pasting) MAYBE allow less grades
            # than pupils
            lines_nb = len(lines)
            pupils_nb = self.pupils_nb()
            if pupils_nb != lines_nb:
                do_paste = False
                if pupils_nb > lines_nb:
                    msg = self.tr('There are only {nb1} grades for {nb2} '
                                  'pupils.\nYou must paste as many grades as '
                                  'pupils.').format(nb1=lines_nb,
                                                    nb2=pupils_nb)
                else:
                    msg = self.tr('There are {nb1} grades for only {nb2} '
                                  'pupils.\nYou must paste as many grades as '
                                  'pupils.').format(nb1=lines_nb,
                                                    nb2=pupils_nb)
                run_message_dialog(self.tr('Number of pupils and grades '
                                           'mismatch'),
                                   msg, 'dialog-warning', self.parentw)

            for grade in lines:
                try:
                    self.check_user_entry(
                        grade, forbid_empty_cell=False,
                        forbid_duplicate_content=False,
                        forbid_internal_sep=True,
                        change_is_required=False)
                except ReservedCharsError:
                    do_paste = False
                    run_message_dialog(self.tr('Reserved group of characters'),
                                       self.tr('The group of characters "{}"'
                                               ' has been found in the data '
                                               'you\'re about to paste, but '
                                               'it is reserved for internal '
                                               'use.\nPlease remove it from '
                                               'the data you want to paste '
                                               'before pasting again.\n'
                                               'Pasting grades cancelled.'
                                               ).format(SEP),
                                       'dialog-warning', self.parentw)

            if do_paste:
                names_list = [p[FULLNAME] for p in self.visible_pupils()]
                if self.user_selected_col_nb is None:
                    view = build_view([self.tr('Names')] + names_list,
                                      [self.tr('Grades')] + [L for L in lines],
                                      xalign=[0, 0.5])
                    msg = self.tr('Add following grades?')
                else:
                    col_num = self.user_selected_col_nb
                    prev_grades_list = [
                        self.store[row.path][GRADES]
                        .cols[col_num:col_num + 1] or ['']
                        for row in self.visible_pupils()]
                    prev_grades_list = [item[0] for item in prev_grades_list]

                    def _set_cell_text(column, cell, model, it, ignored):
                        current = model.get_value(it, 1)
                        update = model.get_value(it, 2)
                        weight = int(Pango.Weight.NORMAL)
                        _, bgcolor, _, _ = get_theme_colors()
                        # LATER: appearance is poor, improve it!
                        if update != current:
                            weight = int(Pango.Weight.BOLD)
                            bgcolor = Gdk.RGBA()
                            bgcolor.parse('rgba(255, 179, 218, 255)')
                        cell.set_property('background_rgba', bgcolor)
                        cell.set_property('weight', weight)

                    view = build_view([self.tr('Names')] + names_list,
                                      [self.tr('Grade #{}')
                                       .format(self.user_selected_col_nb + 1)]
                                      + prev_grades_list,
                                      [self.tr('Update')] + [L for L in lines],
                                      xalign=[0, 0.5, 0.5],
                                      set_cell_func=[None, None,
                                                     _set_cell_text])
                    msg = self.tr('Modify following grades?')
                conf_dialog = ConfirmationDialog(
                    self.tr('Please confirm'), self.parentw,
                    message=msg,
                    widget=view)
                response = conf_dialog.run()
                if response not in [Gtk.ResponseType.YES, Gtk.ResponseType.OK]:
                    do_paste = False
                conf_dialog.destroy()

            if do_paste:
                grade_added = False
                if self.user_selected_col_nb is None:
                    # cannot use self.grades_nb in the loop as it's updated
                    # at any commit
                    col_num = self.grades_nb
                    grade_added = True
                else:
                    col_num = self.user_selected_col_nb

                # Cursor change inspired by
                # https://stackoverflow.com/a/9881020/3926735
                self.get_window().set_cursor(
                    Gdk.Cursor.new_from_name(Gdk.Display.get_default(),
                                             'wait'))

                def add_grades(lines):
                    for grade, row in zip(lines, self.visible_pupils()):
                        # TODO: add a progression bar too, at bottom
                        id_value = self.store[row.path][ID]
                        self.store[row.path][GRADES] = \
                            Listing(grade,
                                    data_row=self.store[row.path][GRADES].cols,
                                    position=col_num)
                        self.store[row.path][ALEVEL] = \
                            calculate_attained_level(
                            self.store[row.path][ILEVEL], self.levels,
                            self.grading, self.store[row.path][GRADES],
                            self.special_grades)
                        self.commit_pupil(
                            id_value, ['grades', 'attained_level'])

                    self.status.document_modified = True
                    self.emit('refresh-title-toolbar')

                    self.get_window().set_cursor(None)
                    return False

                GObject.idle_add(add_grades, lines)

                if grade_added:
                    self.add_grades_column()
                    self.emit('grades_columns_changed', 'grade-added',
                              len(self._grades_columns) - 1)

                if isinstance(self.user_selected_col_nb, int):
                    self.on_column_clicked(
                        self.treeview.get_column(GRADES
                                                 + self.user_selected_col_nb))

    def on_remove_grade_clicked(self, widget):
        # shouldn't be None, actually...
        if self.user_selected_col_nb is not None:
            nth = self.user_selected_col_nb
            grades_entered = \
                any(self.store[row.path][GRADES].get(nth)
                    not in [None, '']
                    for row in self.visible_pupils())
            do_remove = True
            if grades_entered:
                conf_dialog = ConfirmationDialog(
                    self.tr('Please confirm'), self.parentw,
                    message=self.tr('Remove the selected grade?'))
                response = conf_dialog.run()
                if response not in [Gtk.ResponseType.YES, Gtk.ResponseType.OK]:
                    do_remove = False
                conf_dialog.destroy()
            if do_remove:
                for row in self.visible_pupils():
                    try:
                        self.store[row.path][GRADES].pop(nth)
                    except IndexError:
                        pass
                    self.store[row.path][ALEVEL] = calculate_attained_level(
                        self.store[row.path][ILEVEL], self.levels,
                        self.grading, self.store[row.path][GRADES],
                        self.special_grades)
                    id_value = self.store[row.path][ID]
                    self.commit_pupil(id_value, ['grades', 'attained_level'])
                self.remove_grades_column()
                self.unselect_col(self.user_selected_col)
                self.set_buttons_sensitivity()
                self.status.document_modified = True
                self.emit('refresh-title-toolbar')
                self.emit('grades_columns_changed', 'grade-removed', nth)

    def on_add_grade_clicked(self, widget):
        self.add_grades_column()
        self.emit('grades_columns_changed', 'grade-added',
                  len(self._grades_columns) - 1)

        GLib.timeout_add(50, self.treeview.set_cursor,
                         Gtk.TreePath(0),
                         self.treeview.get_column(GRADES + self.grades_nb),
                         True)

    def on_insert_clicked(self, widget):
        if not self.started_insertion:
            ListManagerBase.on_insert_clicked(
                self, widget, at='top', col_nb=FULLNAME,
                do_scroll=(self.scrollable_treelist, Gtk.ScrollType.START,
                           False))
            self.set_buttons_sensitivity()

    def on_paste_pupils_clicked(self, widget):
        text = self.clip.wait_for_text()
        if text is None:
            text = self.clip2.wait_for_text()
        if text is not None:
            if '\t' in text:
                sep = '\t'
            else:
                sep = '\n'
            lines = text.strip().split(sep)

            display_empty_lines_warning = False
            do_paste = True
            for name in lines:
                try:
                    self.check_user_entry(
                        name, forbid_empty_cell=True,
                        forbid_duplicate_content=False,
                        forbid_internal_sep=True,
                        change_is_required=False)
                except EmptyContentError:
                    display_empty_lines_warning = True
                except ReservedCharsError:
                    do_paste = False
                    run_message_dialog(self.tr('Reserved group of characters'),
                                       self.tr('The group of characters "{}" '
                                               'has been found in the data '
                                               'you\'re about to paste, but '
                                               'it is reserved for internal '
                                               'use.\nPlease remove it from '
                                               'the data you want to paste '
                                               'before pasting again.\n'
                                               'Pasting pupils\' names '
                                               'cancelled.'
                                               ).format(SEP),
                                       'dialog-warning', self.parentw)
            if do_paste:
                names_view = build_view([self.tr('Names')] + lines)
                conf_dialog = ConfirmationDialog(
                    self.tr('Please confirm'), self.parentw,
                    message=self.tr('Add following pupils?'),
                    widget=names_view)
                response = conf_dialog.run()
                if response not in [Gtk.ResponseType.YES, Gtk.ResponseType.OK]:
                    do_paste = False
                conf_dialog.destroy()

            if do_paste:
                # Cursor change inspired by
                # https://stackoverflow.com/a/9881020/3926735
                self.get_window().set_cursor(
                    Gdk.Cursor.new_from_name(Gdk.Display.get_default(),
                                             'wait'))

                if display_empty_lines_warning:
                    lines = [L for L in lines if L != '']
                    run_message_dialog(self.tr('Empty lines'),
                                       self.tr('The empty lines that have '
                                               'been found in the data you '
                                               'want to paste\nhave been '
                                               'automatically removed.'),
                                       'dialog-warning', self.parentw)

                added_ids = []

                def add_pupils(lines):
                    # Remember the possible selection before adding pupils
                    col = self.treeview.get_cursor()[1]
                    model, paths = self.selection.get_selected_rows()
                    ref_selected = None
                    if paths:
                        ref_selected = Gtk.TreeRowReference.new(model,
                                                                paths[0])

                    # THIS BELONGS TO A NOT WORKING WORKAROUND, SEE BELOW
                    # ref_last = None
                    # visible_pupils = self.visible_pupils()
                    # if visible_pupils:
                    #     ref_last = Gtk.TreeRowReference.new(
                    #         self.store, visible_pupils[-1].get_path())

                    for name in lines:
                        fill_values = self.default_row_values
                        fill_values[FULLNAME] = name
                        self.store.append(fill_values)
                        new_id = self.commit_pupil(None, ['fullname'])
                        added_ids.append(new_id)

                    self.class_filter.refilter()
                    self.set_buttons_sensitivity()

                    # If the treeview is embedded with an empty grid at its
                    # right to prevent its rightest column to expand, then
                    # the next lines are a work around to force the treeview
                    # to refresh after having pasted pupils.
                    if col is not None:
                        # THIS IS A WORKAROUND FOR THE CASE DESCRIBED HERE:
                        # https://stackoverflow.com/q/72634344/3926735
                        # We briefly click on the first row of the treeview
                        # to ensure the first rows will not remain hidden.
                        GLib.timeout_add(50, self.treeview.set_cursor,
                                         Gtk.TreePath(0), col, False)

                        # THIS NEXT PART IS FOR THE CASE OF LINES AT THE END
                        # THAT DO NOT SHOW UP AFTER PASTING LINES AT START; IT
                        # CONSISTS OF CLICKING ON THE LAST (before pasting)
                        # LINE BUT IT HAS NO EFFECT
                        # We briefly click on the last row of the treeview
                        # to ensure the last rows will not remain hidden.
                        # if ref_last:
                        #     GLib.timeout_add(75, self.treeview.set_cursor,
                        #                      ref_last.get_path(), col,
                        #                      False)

                        # Then we click back to the previously selected row
                        # (if any)
                        if ref_selected:
                            GLib.timeout_add(100, self.treeview.set_cursor,
                                             ref_selected.get_path(), col,
                                             False)

                    self.emit('refresh-title-toolbar')
                    self.emit('pupils-list-changed', 'add', self.classname,
                              ', '.join([str(i) for i in added_ids]))

                    self.get_window().set_cursor(None)
                    return False

                GObject.idle_add(add_pupils, lines)

    def on_remove_clicked(self, widget):
        pupils_to_delete = []
        commit_changes = False
        model, paths = self.selection.get_selected_rows()
        refs = [Gtk.TreeRowReference.new(model, path) for path in paths]
        removed_ids = []
        for ref in refs:
            pupil_id = model.get(model.get_iter(ref.get_path()), 0)[0]
            removed_ids.append(pupil_id)
            for row in self.visible_pupils():
                if row[ID] == pupil_id:
                    cl = self.store[row.path][CLASSES].split(',')
                    cl = [_.strip() for _ in cl]
                    classes_left = [_ for _ in cl if _ != self.classname]
                    if classes_left:  # only remove the pupil from this class
                        self.store[row.path][CLASSES] \
                            = Listing(classes_left).joined()
                        pupil_id = self.store[row.path][ID]
                        self.commit_pupil(pupil_id, ['classnames'])
                        commit_changes = True
                    else:  # the pupil had no other class
                        pupils_to_delete.append(row)

        if pupils_to_delete:
            do_remove = False
            if len(pupils_to_delete) == 1:
                msg = self.tr('Remove the selected pupil?')
            else:
                msg = self.tr('Remove the selected pupils?')
            conf_dialog = ConfirmationDialog(self.tr('Please confirm'),
                                             self.parentw, message=msg)
            response = conf_dialog.run()
            if response in [Gtk.ResponseType.YES, Gtk.ResponseType.OK]:
                do_remove = True
            conf_dialog.destroy()
            if do_remove:
                for row in pupils_to_delete:
                    pupil_id = self.store[row.path][ID]
                    self.store.remove(row.iter)
                    pupil_in_db = self.db.session.query(Pupils).get(pupil_id)
                    self.db.session.delete(pupil_in_db)
                commit_changes = True

        if commit_changes:
            self.db.session.commit()
            self.status.document_modified = True
            self.set_buttons_sensitivity()
            self.emit('refresh-title-toolbar')
            self.emit('pupils-list-changed', 'remove', self.classname,
                      ', '.join([str(i) for i in removed_ids]))

    def on_edit_level_clicked(self, widget):
        dialog = ComboDialog(self.tr('Change initial level'),
                             '', self.levels, self.parentw)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            model, paths = self.selection.get_selected_rows()
            for path in paths:
                self.on_initial_level_edited(widget, path, dialog.choice)
        dialog.destroy()

    def on_edit_class_clicked(self, widget):
        selected_classes = []
        selected_pupils = []
        model, paths = self.selection.get_selected_rows()
        refs = []
        for path in paths:
            refs.append(Gtk.TreeRowReference.new(model, path))
        for ref in refs:
            pupil_id = model.get(model.get_iter(ref.get_path()), 0)[0]
            for row in self.visible_pupils():
                if row[ID] == pupil_id:
                    cl = self.store[row.path][CLASSES].split(',')
                    cl = [_.strip() for _ in cl]
                    selected_classes += cl
                    selected_pupils.append(row)
        selected_classes = list(set(selected_classes))

        other_classes = [cl for cl in self.classes
                         if cl not in selected_classes]

        if other_classes:
            dialog = ComboDialog(self.tr('Add to another class'),
                                 '', other_classes, self.parentw)
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                added_ids = []
                for p in selected_pupils:
                    cl = self.store[p.path][CLASSES].split(',')
                    cl = [_.strip() for _ in cl]
                    new_classes_list = ', '.join(sorted(cl + [dialog.choice]))
                    self.store[p.path][CLASSES] = new_classes_list
                    pupil_id = self.store[p.path][ID]
                    self.commit_pupil(pupil_id, ['classnames'])
                    added_ids.append(pupil_id)
                self.status.document_modified = True
                self.emit('refresh-title-toolbar')
                self.emit('pupils-list-changed', 'add', dialog.choice,
                          ', '.join([str(i) for i in added_ids]))
            dialog.destroy()
        else:
            run_message_dialog(self.tr('Impossible operation'),
                               self.tr('You selected all available classes, '
                                       'there is no class left to attribute.'),
                               'dialog-error', self.parentw)

    def get_selected_col(self):
        return self.treeview.get_column(GRADES + self.user_selected_col_nb)

    def select_col(self, col):
        _, _, fg, bg = get_theme_colors()  # only the "selected" colors
        fg = convert_gdk_rgba_to_hex(fg)
        bg = convert_gdk_rgba_to_hex(bg)
        self.user_selected_col_nb = col.grade_nb
        self.user_selected_col = col
        selected_title = Gtk.Label()
        selected_title.set_markup(
            r'<span fgcolor="{}" bgcolor="{}">{}</span>'
            .format(fg, bg, '#{}'.format(col.grade_nb + 1)))
        col.set_widget(selected_title)
        selected_title.show()
        self.renderer_name.props.editable = False

    def unselect_col(self, col):
        if col is not None:
            col.set_widget(None)
            col.set_title('#{}'.format(col.grade_nb + 1))
        self.user_selected_col_nb = None
        self.user_selected_col = None
        self.renderer_name.props.editable = True

    def on_column_clicked(self, col):
        if self.unselected_rows is None:
            self.unselected_rows = \
                [t.to_string() for t in self.selection.get_selected_rows()[1]]
        self.selection.unselect_all()
        if self.user_selected_col_nb is None:  # no selected col yet
            self.select_col(col)
        else:
            if col.grade_nb == self.user_selected_col_nb:  # unselect col
                self.unselect_col(col)
                if self.unselected_rows is not None:  # give selection back
                    for i in self.unselected_rows:
                        self.selection.select_path(Gtk.TreePath(int(i)))
                self.unselected_rows = None
            else:  # change selected col
                prev_col = self.get_selected_col()
                new_col = col
                self.unselect_col(prev_col)
                self.select_col(new_col)
        self.set_buttons_sensitivity()
        # LATER: maybe also show col's cells selected or highlighted
        # to make it obvious

    def on_name_edited(self, widget, path, new_text):
        accepted, id_value = self.on_cell_edited(
            widget, path, new_text, forbid_empty_cell=True, col_nb=FULLNAME,
            forbid_duplicate_content=False, forbid_internal_sep=False)

        if accepted:
            self.commit_pupil(id_value, ['fullname'])
            if id_value:
                pupil = self.db.session.query(Pupils).get(id_value)
                for cl in pupil.classnames:
                    self.emit('pupils-list-changed', 'rename', cl,
                              str(id_value))
            self.status.document_modified = True
            self.emit('refresh-title-toolbar')
            self.set_buttons_sensitivity()

    def on_included_toggled(self, cell_renderer, path):
        _, path = self.get_path_from_id(self.visible_pupils()[int(path)][ID])
        self.store[path][INCLUDED] = not self.store[path][INCLUDED]
        id_value = self.store[path][ID]
        self.commit_pupil(id_value, ['included'])
        action = {True: 'include',
                  False: 'exclude'}[self.store[path][INCLUDED]]
        self.emit('pupils-list-changed', action, self.store[path][CLASSES],
                  str(id_value))
        self.status.document_modified = True
        self.emit('refresh-title-toolbar')

    def on_initial_level_edited(self, widget, path, new_text):
        _, path = self.get_path_from_id(self.visible_pupils()[int(path)][ID])
        if new_text != self.store[path][ILEVEL]:
            ilevel = new_text
            self.store[path][ILEVEL] = ilevel
            grades = self.store[path][GRADES]
            self.status.document_modified = True
            self.store[path][ALEVEL] = calculate_attained_level(
                ilevel, self.levels, self.grading, grades, self.special_grades)
            self.commit_pupil(self.store[path][ID],
                              ['initial_level', 'attained_level'])
            self.emit('refresh-title-toolbar')
        self.post_edit_cleanup()
        self.set_buttons_sensitivity()

    def on_grade_edited(self, widget, path, new_text):
        id_value, model, treeiter, row = self.get_selection_info()
        _, path = self.get_path_from_id(self.visible_pupils()[int(path)][ID])
        pupil = self.db.session.query(Pupils).get(id_value)
        col = self.treeview.get_cursor()[1]
        if pupil.grades is None:
            kwargs = None
        else:
            kwargs = {'data_row': pupil.grades, 'position': col.grade_nb}
        last_row = None
        try:
            old_text = model.get(treeiter, GRADES)[0][col.grade_nb]
        except IndexError:
            old_text = ''
        if self.treeview.get_visible_range() is not None:
            last_row = self.treeview.get_visible_range()[1]
        accepted, id_value = \
            self.on_cell_edited(widget, path, new_text, col_nb=GRADES,
                                forbid_empty_cell=False,
                                forbid_duplicate_content=False,
                                do_cleanup=False,
                                cell_store_type=Listing,
                                cell_store_kwargs=kwargs,
                                old_text=old_text)
        if accepted:
            self.store[path][ALEVEL] = calculate_attained_level(
                pupil.initial_level, self.levels, self.grading,
                self.store[path][GRADES], self.special_grades)
            self.commit_pupil(id_value, ['grades', 'attained_level'])
            time.sleep(0.1)
            if col is not None and last_row is not None:
                position = int(row.to_string())
                last_position = int(last_row.to_string())
                next_val = 'undefined'  # Could be any str except ''
                while position < last_position:
                    next_row = Gtk.TreePath(position + 1)
                    try:
                        next_val = self.store[next_row][GRADES]\
                            .cols[col.grade_nb]
                    except IndexError:
                        next_val = ''
                    if next_val in ['', None]:
                        break
                    else:
                        position += 1
                if next_val in ['', None]:
                    GLib.timeout_add(50, self.treeview.set_cursor,
                                     next_row, col, True)
                else:
                    self.on_editing_canceled(None)
            self.emit('refresh-title-toolbar')
        else:  # Unaccepted text (e.g. internal separator was rejected)
            # Simply set cursor on the same cell again
            GLib.timeout_add(50, self.treeview.set_cursor, row, col, True)

    def commit_pupil(self, id_value, attrnames=None):
        # TODO: add a method that would do most of this job, but not commit
        # (like 'add_pupil'), that this method would re-use in order to
        # commit. This would be helpful in cases where a bunch of pupils is
        # added at once (then only one commit at the end).
        # Or maybe a unique method that would deal with a bunch of pupils?
        _, path = self.get_path_from_id(id_value)
        new = False
        if attrnames is None:
            attrnames = []
        if id_value in ['', None]:
            new = True
            pupil = Pupils(classnames=[self.classname],
                           included=self.store[path][INCLUDED],
                           fullname=self.store[path][FULLNAME],
                           initial_level=self.store[path][ILEVEL],
                           attained_level=self.store[path][ALEVEL],
                           grades=self.store[path][GRADES])
            self.db.session.add(pupil)
        else:
            pupil = self.db.session.query(Pupils).get(id_value)
            for attrname in attrnames:
                col_nb = PUPILS_COL_NBS[attrname]
                data = self.store[path][col_nb]
                if attrname == 'classnames':
                    data = Listing([_.strip() for _ in data.split(',')])
                setattr(pupil, attrname, data)
        self.db.session.commit()
        self.status.document_modified = True
        if new:
            self.store[path][ID] = str(pupil.id)
        return pupil.id
