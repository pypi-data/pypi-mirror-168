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

import sys
import glob
import subprocess
from pathlib import Path
from shutil import copyfile
import gi

try:
    gi.require_version('Gtk', '3.0')
except ValueError:
    raise
else:
    from gi.repository import GLib, GObject

from pikepdf import Pdf
from sqlalchemy.sql.expression import and_

from cotinga.models import Pupils
from .errors import NoTemplateFoundError
from .errors import MixedTemplatesFormatsError
from cotinga.core import doc_setup
from cotinga.core.presets import TEMPLATE_PREFIX


def lower(s):
    return s.lower()


def none(s):
    return s


def title(s):
    return s.title()


def capitalize(s):
    return s.capitalize()


belt_process = {'none': none, 'lower': lower, 'title': title,
                'capitalize': capitalize}


def tex_compiler_is_not_available():
    try:
        subprocess.run('lualatex --version'.split())
    except FileNotFoundError:
        return True
    return False


def list_levels(classname, pupils, db):
    """List levels of the pupils, in the same order as pupils."""
    levels = []
    for fullname in pupils:
        levels.append(db.session.query(Pupils).filter(
            and_(Pupils.included == True,  # noqa
                 Pupils.classnames.contains([classname]),
                 Pupils.fullname == fullname)).all()[0].attained_level)
    all_levels = doc_setup.load()['levels']
    # TODO: handle the pupils that have got to the last level, the next line
    # raises an IndexError for them since there's no next level...
    levels = [all_levels[all_levels.index(L) + 1] for L in levels]
    return levels


def check_templates_fmt(dirpath, levels):
    """
    Tell whether template files are singletons or grouped in pairs.

    :param dirpath: the directory where the templates can be found
    :type dirpath: pathlib.Path()
    :param levels: the list of pupils' levels, matching the pupils' list
    :type levels: list
    """
    singletons = pairs = False
    if any(True if (Path(dirpath) / f'{TEMPLATE_PREFIX()}{L}.tex').is_file()
           else False
           for L in levels):
        singletons = True
    if any(True if (Path(dirpath) / f'{TEMPLATE_PREFIX()}{L}0.tex').is_file()
           else False
           for L in levels):
        pairs = True
    if singletons and pairs:
        raise MixedTemplatesFormatsError()
    elif not singletons and not pairs:
        raise NoTemplateFoundError()
    elif singletons:
        return 'singletons'
    else:
        return 'pairs'


def missing_templates(dirpath, levels, fmt):
    """
    List or set of the missing template files.

    :param dirpath: the directory where the templates can be found
    :type dirpath: pathlib.Path()
    :param levels: the list of pupils' levels, matching the pupils' list
    :type levels: list
    """
    dirpath = Path(dirpath)
    prefix = TEMPLATE_PREFIX()
    if fmt == 'singletons':
        return [L for L in levels
                if not (dirpath / f'{prefix}{L}.tex').is_file()]
    else:  # fmt == 'pairs'
        return set([L for L in levels
                    if not (dirpath / f'{prefix}{L}0.tex').is_file()]
                   + [L for L in levels
                      if not (dirpath / f'{prefix}{L}1.tex').is_file()])


def incorrect_templates(dirpath, levels, fmt):
    """
    Set of the incorrect template files.

    :param dirpath: the directory where the templates can be found
    :type dirpath: pathlib.Path()
    :param levels: the list of pupils' levels, matching the pupils' list
    :type levels: list
    """
    dirpath = Path(dirpath)
    prefix = TEMPLATE_PREFIX()
    if fmt == 'singletons':
        return set([L for L in levels
                    if '<FULLNAME>'
                    not in (dirpath / f'{prefix}{L}.tex').read_text()])
    else:  # fmt == 'pairs'
        return set([L for L in levels
                    if '<FULLNAME>'
                    not in (dirpath / f'{prefix}{L}0.tex').read_text()]
                   + [L for L in levels
                      if '<FULLNAME>'
                      not in (dirpath / f'{prefix}{L}1.tex').read_text()])


def update_progress(progressbar, i, total, text=None):
    if text:
        progressbar.set_show_text(True)
    else:
        progressbar.set_show_text(False)
    progressbar.set_text(text)
    progressbar.set_fraction(i / total)
    return False


class MergingOperation(GObject.Object):

    @GObject.Signal
    def merging_finished(self):
        """Notify that the merging is finished."""

    @GObject.Signal
    def merging_aborted(self):
        """Notify that the merging has been aborted (compilation failed)."""

    def __init__(self, tr, *kwargs):
        GObject.Object.__init__(self, *kwargs)
        self.filename = ''
        self.tr = tr
        self.title = ''
        self.process_belt_tag = 'none'

    def merge_tests(self, dirpath, testname, classname, pupils, levels, fmt,
                    label, progressbar, merged_name):
        """
        Create the individual test sheets, compile and merge them all.

        The templates are supposed to exist and be correct.

        :param dirpath: the directory where the templates can be found
        :type dirpath: pathlib.Path()
        :param testname: the testname, as provided by the user
        :type testname: str
        :param classname: the class' name
        :type classname: str
        :param pupils: the list of pupils' fullnames, in the order they have to
        be processed
        :type pupils: list
        :param levels: the list of pupils' levels, matching the pupils' list
        :type levels: list
        :param label: a label to show the current step to the user
        :type label: Gtk.Label
        :param progressbar: the progress bar to be displayed
        :type progressbar: Gtk.ProgressBar
        """
        dirpath = Path(dirpath)
        # tests_dir is assumed to not exist yet and that we have rights to
        # write files in it
        tests_dir = Path(dirpath / testname)
        tests_dir.mkdir(parents=True)

        eps_files = glob.glob(f'{str(dirpath)}/*.eps')
        for i, f in enumerate(eps_files):
            copyfile(f, tests_dir / Path(f).name)

        GLib.idle_add(update_progress, progressbar, 0, 1,
                      text=self.tr('Creation of the tests...'))
        total = len(pupils)
        tests_paths = []
        pdf_paths = []
        counters = {L: 0 for L in levels}
        for i, couple in enumerate(zip(pupils, levels)):
            GLib.idle_add(update_progress, progressbar, i, total)
            fullname, level = couple
            testpath = tests_dir / f'{i:02} {fullname}.tex'
            pdf_paths.append(tests_dir / f'{i:02} {fullname}.pdf')
            tests_paths.append(testpath)
            if fmt == 'singletons':
                filename = f'{TEMPLATE_PREFIX()}{level}.tex'
            else:  # fmt == 'pairs'
                parity = counters[level] % 2
                filename = f'{TEMPLATE_PREFIX()}{level}{parity}.tex'
                counters[level] += 1
            template_path = dirpath / filename
            belt = belt_process[self.process_belt_tag](level)
            testpath.write_text(template_path.read_text()
                                .replace('<TITLE>', self.title)
                                .replace('<BELT>', belt)
                                .replace('<FULLNAME>', fullname)
                                .replace('<CLASSNAME>', classname))

        GLib.idle_add(update_progress, progressbar, 0, 1)
        for i, path in enumerate(tests_paths):
            self.filename = path.name
            GLib.idle_add(update_progress, progressbar, i, total,
                          self.filename)
            msg = self.tr('Compiling {filename}')
            msg = msg.format(filename=self.filename)
            p = subprocess.Popen(['lualatex', '-interaction', 'nonstopmode',
                                  str(path.name)],
                                 cwd=str(tests_dir), stdout=sys.stderr)
            errorcode = p.wait()
            if errorcode:
                self.emit('merging-aborted')
                return
            # Also check a pdf file has been created? Without any error,
            # it should have been.

        GLib.idle_add(update_progress, progressbar, 0, 1)
        pdf = Pdf.new()
        for i, path in enumerate(pdf_paths):
            GLib.idle_add(update_progress, progressbar, i, total)
            with Pdf.open(path) as src:
                pdf.pages.extend(src.pages)
        pdf.save(tests_dir / merged_name)
        pdf.close()
        GLib.idle_add(update_progress, progressbar, total, total)
        self.emit('merging-finished')
        return True
