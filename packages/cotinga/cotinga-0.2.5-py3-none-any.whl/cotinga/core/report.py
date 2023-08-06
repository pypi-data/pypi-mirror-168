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
from datetime import datetime
from gettext import translation

from pikepdf import Pdf
from microlib import grouper
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.platypus import PageBreak, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from . import doc_setup
from .env import REPORT_FILE, LOCALEDIR, L10N_DOMAIN
from . import prefs

DARK_GRAY = colors.HexColor(0x333333)
DIM_GRAY = colors.HexColor(0x808080)


def rework_data(data, max_nb_per_col):
    tr = translation(L10N_DOMAIN, LOCALEDIR,
                     [prefs.load()['language']]).gettext
    col_data = []
    spans = []
    classes = set()
    for col in data:
        title = tr('{level} ({nb})').format(level=col[0], nb=col[1])
        names = sorted([pupil.fullname for pupil in col[2]])
        # classes need to be fixed now
        classes |= set([cl for pupil in col[2] for cl in pupil.classnames])
        for i, lst in enumerate(grouper(names, max_nb_per_col, padvalue='')):
            if i:
                new_col = ['']
                spans.append(True)
            else:
                new_col = [title]  # copy title in the first column
                spans.append(False)
            new_col += lst
            col_data.append(new_col)
    maxi = max([len(item) for item in col_data] + [0])
    report_data = []
    for i in range(maxi):
        new_row = [item[i:i + 1] or ['']
                   for item in col_data]
        new_row = [p[0] for p in new_row]
        if any(name != '' for name in new_row):
            report_data.append(new_row)
    spans.append(False)
    return report_data, spans, classes


def workout_spans(spans):
    result = []
    start_span = None
    for i, span in enumerate(spans):
        if start_span is None:
            if span:
                start_span = i - 1
        else:
            if not span:
                result.append(('SPAN', (start_span, 0), (i - 1, 0)))
                start_span = None
    return result


def slice_table(table, n):
    """
    Separate a table into a table of the first n columns and a second with
    remaining columns.

    :param table: the table to slice
    :param n: the number of the last column to take into the first part. It is
    assumed to be a positive integer
    """
    n = int(n)
    if n < 0:
        raise ValueError('argument n is assumed to be positive')
    if not table:
        return [], []
    else:
        length = len(table[0])
        if n >= length - 1:
            return table, []
        else:
            t1 = [row[0:n + 1] for row in table]
            t2 = [row[n + 1:length] for row in table]
            return t1, t2


def split_table(table, n):
    """
    Separate a table into a tables of n columns. The last will only have the
    remaining columns.

    :param table: the table to split
    :param n: the number of columns of each table. It is assumed to be a
    positive integer
    """
    remaining = table
    slices = []
    while remaining:
        one_slice, remaining = slice_table(remaining, n - 1)
        slices.append(one_slice)
    return slices


def split_spans(spans, n):
    spans = spans[:-1]  # remove the last False
    chunks = [spans[x:x + n] for x in range(0, len(spans), n)]
    chunks = [list(c) + [False] for c in chunks]
    for c in chunks:
        c[0] = False
    return chunks


def determine_max_cols(width):
    width = float(width)
    if 3.7 <= width < 4.2:
        return 7
    elif 4.2 <= width < 4.9:
        return 6
    elif 4.9 <= width < 5.9:
        return 5
    elif 5.9 <= width <= 7.4:
        return 4
    else:
        raise ValueError(
            'width is assumed to be comprised between 3.7 and 7.4')


def classes_list_str(tr, classes):
    last_sep = ' {} '.format(tr('and'))
    classes_list = last_sep.join(sorted(list(classes)))
    classes_list = classes_list.replace(last_sep, ', ', len(classes) - 2)
    return classes_list


def build_header(tr, title, classes, date_fmt, stylesheet):
    title_style = stylesheet['Title']
    title_style.spaceAfter = 0.5 * cm
    date = datetime.now().strftime(date_fmt)
    classes_list = classes_list_str(tr, classes)
    title = title.replace('<CLASSES>', classes_list).replace('<DATE>', date)
    return Paragraph(title, title_style)


def build_subheader(tr, subtitle, classes, date_fmt, stylesheet):
    h2_style = stylesheet['Heading3']
    h2_style.spaceAfter = 0.5 * cm
    date = datetime.now().strftime(date_fmt)
    classes_list = classes_list_str(tr, classes)
    subtitle = subtitle.replace('<CLASSES>', classes_list)\
        .replace('<DATE>', date)
    return Paragraph(subtitle, h2_style)


def fix_columns_titles(data):
    for i, table in enumerate(data):
        if i >= 1:
            if table[0][0] == '':  # first title is empty
                # replace by the last one from previous table
                table[0][0] = data[i - 1][0][-1]


def build_tables(data, spans, max_cols, colwidth):
    data = split_table(data, max_cols)
    spans = split_spans(spans, max_cols)
    fix_columns_titles(data)

    tables = []

    for table, s in zip(data, spans):
        ncol = len(table[0])
        nrow = len(table)

        t = Table(table, ncol * [colwidth * cm], nrow * [0.5 * cm])

        col_separators = [('LINEAFTER', (i, 0), (i, nrow), 1, DIM_GRAY)
                          for i in range(ncol - 1)
                          if not s[(i + 1)]]

        t.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                               ('TEXTCOLOR', (0, 0), (-1, -1), DARK_GRAY),
                               ('LINEABOVE', (0, 1), (ncol, 1), 1, DIM_GRAY)
                               ] + col_separators + workout_spans(s)))
        tables.append(t)
        # print(f'WORKED OUT SPANS= {workout_spans(spans)}')

    return tables


def collate_elements(title, subtitle, classes, date_fmt, tables_per_page,
                     tables):
    stylesheet = getSampleStyleSheet()
    tr = translation(L10N_DOMAIN, LOCALEDIR,
                     [prefs.load()['language']]).gettext
    elements = []
    elements.append(build_header(tr, title, classes, date_fmt, stylesheet))
    elements.append(build_subheader(tr, subtitle, classes, date_fmt,
                                    stylesheet))
    pages_nb = 1
    for i, t in enumerate(tables):
        elements.append(t)
        if i != len(tables) - 1:
            if (i + 1) % tables_per_page:
                elements.append(Spacer(1, 15))
            else:
                elements.append(PageBreak())
                pages_nb += 1
    return pages_nb, elements


def build(data):
    report_setup = doc_setup.load()['report']
    title = report_setup['title']
    subtitle = report_setup['subtitle']
    max_rows = report_setup['max_rows']
    date_fmt = report_setup['date_fmt']
    colwidth = report_setup['col_width']
    max_tables = report_setup['max_tables']

    data, spans, classes = rework_data(data, max_rows)
    max_cols = determine_max_cols(colwidth)
    tables = build_tables(data, spans, max_cols, colwidth)

    # create and write the document to disk
    doc = SimpleDocTemplate(str(REPORT_FILE), pagesize=landscape(A4),
                            leftMargin=0 * cm, rightMargin=0 * cm,
                            topMargin=0 * cm, bottomMargin=0 * cm)

    pages_nb, content = collate_elements(title, subtitle, classes, date_fmt,
                                         max_tables, tables)
    doc.build(content)
    return pages_nb


def splitname(report_file, n):
    parent = Path(report_file).parent
    f = Path(report_file).stem
    return parent / f'{str(f)}{n}.pdf'


def split(report_file):
    """Split the report in one-page pdf files."""
    with Pdf.open(report_file) as pdf:
        for n, page in enumerate(pdf.pages):
            with Pdf.new() as dst:
                dst.pages.append(page)
                dst.save(splitname(report_file, n))


def cleanup(report_file):
    """Delete one-page pdf relating to the original report file."""
    n = 0
    while(splitname(report_file, n).is_file()):
        splitname(report_file, n).unlink()
        n += 1
