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
    gi.require_version('Poppler', '0.18')
except ValueError:
    raise
else:
    from gi.repository import Gtk

from cotinga.core import doc_setup, constants
from cotinga.core.tools import cellfont_fmt
from cotinga.core.env import get_theme_colors
from cotinga.gui.core.list_manager import ListManagerBase


# Column numbers of the store
ID, INCLUDED, CLASSES, FULLNAME, ILEVEL, ALEVEL, GRADES = (0, 1, 2, 3, 4, 5, 6)

STEPS = constants.NUMERIC_STEPS


def set_cell_fgcolor(column, cell, model, it, ignored):
    """Turn not included pupils in grey."""
    included = model.get_value(it, INCLUDED)
    if included:
        fgcolor, _, _, _ = get_theme_colors()
        cell.set_property('foreground_rgba', fgcolor)
    else:
        cell.set_property('foreground', 'Grey')


def set_gradecell_text(column, cell, model, it, index):
    docsetup = doc_setup.load()
    obj = model.get_value(it, GRADES)
    if index < len(obj.cols):
        cell_text = obj.cols[index]
        cell.set_property('text', cell_text)
        color, weight = cellfont_fmt(cell_text,
                                     docsetup['special_grades'],
                                     docsetup['grading'])
        cell.set_property('foreground', color)
        cell.set_property('weight', weight)
    else:
        cell.set_property('text', '')


class PupilsView(object):

    def __init__(self):
        self._grades_columns = []
        self._setup_grades_cell_width()
        self._create_grade_renderer()
        self._adjust_grade_renderer()
        self._create_tv_columns_renderers()
        self._adjust_tv_columns_renderers()
        self._create_tv_columns()
        self._adjust_tv_columns()
        self._create_tv_sorted_filtered_model()
        self.build_treeview()

    def _setup_grades_cell_width(self):
        if self.grading['choice'] == 'numeric':
            self.grades_cell_width = \
                len(str(self.grading['maximum'])) \
                + len(STEPS[self.grading['step']]) - 1
        else:  # self.grading['choice'] == 'literal'
            self.grades_cell_width = \
                max([len(item) for item in self.grading['literal_grades']])
        max_special_grades = max([len(item) for item in self.special_grades])
        # 3 is the default minimal value in Gtk (could be omitted here)
        self.grades_cell_width = max(3, max_special_grades + 1,
                                     self.grades_cell_width + 1)

    def _create_grade_renderer(self):
        self.grade_renderer = Gtk.CellRendererText()
        self.grade_renderer.props.max_width_chars = self.grades_cell_width
        # self.grade_renderer.set_alignment(0.5, 0.5)

    def _adjust_grade_renderer(self):
        pass

    def _adjust_grades_column(self, nth):
        pass

    def _create_tv_columns_renderers(self):
        self.renderer_id = Gtk.CellRendererText()
        self.renderer_incl = Gtk.CellRendererToggle()
        self.renderer_class = Gtk.CellRendererText()
        self.renderer_name = Gtk.CellRendererText()
        self.renderer_ilevel = Gtk.CellRendererText()
        self.renderer_alevel = Gtk.CellRendererText()

    def _adjust_tv_columns_renderers(self):
        pass

    def _create_tv_columns(self):
        self.col_id = Gtk.TreeViewColumn('id', self.renderer_id, text=0)
        self.col_id.set_cell_data_func(self.renderer_id, set_cell_fgcolor, '')
        self.col_id.set_visible(self.status.show_col_id)

        self.col_incl = Gtk.TreeViewColumn(self.tr('Included'),
                                           self.renderer_incl, active=1)

        self.col_class = Gtk.TreeViewColumn(self.tr('Class'),
                                            self.renderer_class, text=2)
        self.col_class.set_cell_data_func(self.renderer_class,
                                          set_cell_fgcolor, '')

        self.col_name = Gtk.TreeViewColumn(self.tr('Name'), self.renderer_name,
                                           text=3)
        self.col_name.set_cell_data_func(self.renderer_name, set_cell_fgcolor,
                                         '')

        self.col_ilevel = Gtk.TreeViewColumn(self.tr('Initial level'),
                                             self.renderer_ilevel, text=4)
        self.col_ilevel.set_cell_data_func(self.renderer_ilevel,
                                           set_cell_fgcolor, '')

        self.col_alevel = Gtk.TreeViewColumn(self.tr('Attained level'),
                                             self.renderer_alevel, text=5)
        self.col_alevel.set_cell_data_func(self.renderer_alevel,
                                           set_cell_fgcolor, '')

    # @abstractmethod
    def _adjust_tv_columns(self):
        """Must be redefined"""

    def _create_tv_sorted_filtered_model(self):
        self.class_filter = self.store.filter_new()
        self.class_filter.set_visible_func(self.class_filter_func)
        self.sorted_filtered_model = Gtk.TreeModelSort(model=self.class_filter)
        self.sorted_filtered_model.set_sort_column_id(FULLNAME,
                                                      Gtk.SortType.ASCENDING)

    def build_treeview(self):
        self.treeview = Gtk.TreeView.new_with_model(self.sorted_filtered_model)
        # As original treeview is modified, it's necessary to reconnect it
        self.selection.connect('changed', self.on_tree_selection_changed)
        self.selection.set_mode(Gtk.SelectionMode.MULTIPLE)

        for i, col in enumerate([self.col_id, self.col_incl, self.col_class,
                                 self.col_name, self.col_ilevel,
                                 self.col_alevel]):
            # TODO: do not set a minimum width (or not hardcoded at least)
            # instead, check properties of Gtk.TreeViewColumn objects and see
            # what's possible
            # col.set_min_width(100)
            self.treeview.append_column(col)

        for i in range(self.grades_nb):
            self.add_grades_column()

    def add_grades_column(self):
        nth = len(self._grades_columns)
        new_col = Gtk.TreeViewColumn(f'#{nth + 1}', self.grade_renderer)
        new_col.set_cell_data_func(self.grade_renderer, set_gradecell_text,
                                   nth)
        new_col.set_min_width(80)
        # new_col.set_alignment(0.5)
        new_col.grade_nb = nth
        self._grades_columns.append(new_col)
        self._adjust_grades_column(nth)
        self.treeview.append_column(self._grades_columns[nth])

    def remove_grades_column(self):
        # We actually remove the last column (to have one column less);
        # as the store will have less data, the remaining columns will
        # display the remaining data, that's all
        last = self.treeview.get_column(GRADES + len(self._grades_columns) - 1)
        self.treeview.remove_column(last)
        self._grades_columns.pop(-1)


class MetaView(type(ListManagerBase), type(PupilsView)):
    pass
