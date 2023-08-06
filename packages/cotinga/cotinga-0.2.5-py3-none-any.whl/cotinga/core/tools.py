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

from pathlib import Path
from decimal import Decimal
from tarfile import is_tarfile
from gettext import translation
from decimal import InvalidOperation

import gi
try:
    gi.require_version('Gtk', '3.0')
    gi.require_version('Pango', '1.0')
except ValueError:
    raise
else:
    from gi.repository import Gtk, Pango

from . import prefs, constants
from .env import L10N_DOMAIN, LOCALEDIR

STEPS = constants.NUMERIC_STEPS

MM_BELTS = ['01_white1_exam', '02_white2_exam', '03_yellow_exam',
            '04_yellow1_exam', '05_yellow2_exam', '06_orange_exam',
            '07_orange1_exam', '08_orange2_exam', '09_green_exam']


def is_cot_file(path):
    return Path(path).is_file() and is_tarfile(path)


def cot_filter(filter_info, data):
    path = filter_info.filename
    return is_cot_file(path) and path.endswith('.tgz')


def add_filter_any(dialog):
    tr = translation(L10N_DOMAIN, LOCALEDIR,
                     [prefs.load()['language']]).gettext
    filter_any = Gtk.FileFilter()
    filter_any.set_name(tr('Any files'))
    filter_any.add_pattern('*')
    dialog.add_filter(filter_any)


def add_cot_filters(dialog):
    tr = translation(L10N_DOMAIN, LOCALEDIR,
                     [prefs.load()['language']]).gettext

    filter_cot = Gtk.FileFilter()
    filter_cot.set_name(tr('Cotinga files'))
    filter_cot.add_custom(Gtk.FileFilterFlags.FILENAME, cot_filter, None)
    dialog.add_filter(filter_cot)

    add_filter_any(dialog)


def add_pdf_filters(dialog):
    tr = translation(L10N_DOMAIN, LOCALEDIR,
                     [prefs.load()['language']]).gettext

    filter_pdf = Gtk.FileFilter()
    filter_pdf.set_name(tr('Any pdf file'))
    filter_pdf.add_mime_type('application/pdf')
    dialog.add_filter(filter_pdf)

    add_filter_any(dialog)


def check_grade(cell_text, special_grades, grading):
    result = (True, True)
    if cell_text in special_grades:
        result = (True, False)
    else:
        if grading['choice'] == 'numeric':
            if cell_text in ['', None]:
                result = (False, False)
            else:
                try:
                    nb = Decimal(str(cell_text).replace(',', '.'))
                except InvalidOperation:
                    result = (False, False)
                else:
                    if (nb < Decimal(grading['minimum'])
                            or nb > Decimal(grading['maximum'])
                            or nb % Decimal(STEPS[grading['step']])):
                        result = (False, False)
        else:  # grading['choice'] is 'literal'
            if cell_text not in grading['literal_grades']:
                result = (False, False)
    return result


def cellfont_fmt(cell_text, special_grades, grading):
    # LATER: use theme foreground color instead of black
    paint_it = 'Black'
    weight = int(Pango.Weight.NORMAL)
    accepted, regular = check_grade(cell_text, special_grades, grading)
    if accepted:
        if not regular:
            paint_it = 'Grey'
    else:
        paint_it = 'Firebrick'
        weight = int(Pango.Weight.BOLD)
    return (paint_it, weight)


def grade_ge_edge(grading, grade, special_grades):
    accepted, regular = check_grade(grade, special_grades, grading)
    if accepted and regular:
        if grading['choice'] == 'numeric':
            edge = grading['edge_numeric']
            return Decimal(str(grade).replace(',', '.')) >= Decimal(edge)
        else:  # grading['choice'] == 'literal'
            edge = grading['edge_literal']
            return grading['literal_grades'].index(grade) \
                <= grading['literal_grades'].index(edge)
    else:
        return False


def calculate_attained_level(start_level, levels, grading, grades,
                             special_grades):
    # LATER: check start_level belongs to levels? otherwise raise ValueError
    index = levels.index(start_level)
    for grade in grades:
        if grade_ge_edge(grading, grade, special_grades):
            index += 1
    try:
        result = levels[index]
    except IndexError:  # TODO: better handle this situation (last level + 1)
        result = levels[-1]
    return result


def file_uri(file_name):
    return f'file://{str(file_name)}'


def build_view(*cols, xalign=None, set_cell_func=None):
    """
    Example: build_view(['Title1', 'data1', 'data2'],
                        ['Title2', 'data3', 'data4'])

    :param cols: the columns contents, starting with title
    :type cols: list
    :rtype: Gtk.TreeView
    """
    store = Gtk.ListStore(*([str] * len(cols)))
    for i, row in enumerate(zip(*cols)):
        if i:  # we do not add the first data, being the title
            store.append(row)
    view = Gtk.TreeView(store)
    view.props.margin = 10
    view.get_selection().set_mode(Gtk.SelectionMode.NONE)
    for i, col in enumerate(cols):
        rend = Gtk.CellRendererText()
        if xalign is not None:
            rend.props.xalign = xalign[i]
        view_col = Gtk.TreeViewColumn(col[0], rend, text=i)
        if set_cell_func is not None and set_cell_func[i] is not None:
            view_col.set_cell_data_func(rend, set_cell_func[i])
        view.append_column(view_col)
    return view


class Listing(object):

    def __init__(self, data, data_row=None, position=None):
        """
        data may be None or a list or any other type
        prepend must be None or a list
        """
        if data_row is None:
            data_row = []
        if not isinstance(data_row, list):
            raise TypeError('Argument data_row should be a list, found {} '
                            'instead'.format(str(type(data_row))))
        if data is None:
            data = []
        if not isinstance(data, list):
            data = [data]
        self.cols = [item for item in data_row]
        if position is None:
            position = len(self.cols)
        for i, item in enumerate(data):
            retry = True
            while retry:
                try:
                    self.cols[position + i] = item
                except IndexError:
                    self.cols.append('')
                else:
                    retry = False

    def joined(self, sep=', '):
        return sep.join(self.cols)

    def __iter__(self):
        return iter(self.cols)

    def __str__(self):
        return str(self.cols)

    def __repr__(self):
        return 'Listing({})'.format(self.cols)

    def __getitem__(self, key):
        return self.cols[key]

    def __setitem__(self, key, value):
        self.cols[key] = value

    def pop(self, i):
        return self.cols.pop(i)

    def get(self, i, default=None):
        try:
            result = self.cols[i]
        except IndexError:
            result = default
        return result

    def __lt__(self, other):
        return self.cols.__lt__(other)

    def __le__(self, other):
        return self.cols.__le__(other)

    def __eq__(self, other):
        return self.cols.__eq__(other)

    def __ne__(self, other):
        return self.cols.__ne__(other)

    def __gt__(self, other):
        return self.cols.__gt__(other)

    def __ge__(self, other):
        return self.cols.__ge__(other)
