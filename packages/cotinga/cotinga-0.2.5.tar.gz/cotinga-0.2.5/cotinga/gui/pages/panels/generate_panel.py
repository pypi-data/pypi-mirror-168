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

import re
import json
import shutil
from pathlib import Path
from gettext import translation

from pikepdf import Pdf

from cotinga.core import mathmaker
from cotinga.core.env import ICON_THEME, BELTS_JSON
from cotinga.core import doc_setup
from cotinga.gui.core.list_manager import ListManagerPanel
from cotinga.gui.dialogs import FolderSelectDialog
from cotinga.gui.dialogs import run_message_dialog
from cotinga.core.env import LOCALEDIR, L10N_DOMAIN


class GeneratePanel(ListManagerPanel):

    def __init__(self, db, status, prefs, recollections, parentw,
                 mini_items_nb=2):
        # This panel is shown only if mathmaker is available
        self.parentw = parentw
        tr = translation(L10N_DOMAIN, LOCALEDIR, [prefs.language]).gettext

        years_store = Gtk.ListStore(str)
        available_mmyears = mathmaker.available_years()
        for y in available_mmyears:
            years_store.append([y])

        self.mmyear_combo = Gtk.ComboBox.new_with_model(years_store)
        renderer = Gtk.CellRendererText()
        self.mmyear_combo.pack_start(renderer, False)
        self.mmyear_combo.add_attribute(renderer, 'text', 0)
        if recollections.mm_year in available_mmyears:
            self.mmyear_combo.set_active(
                available_mmyears.index(recollections.mm_year))
        else:
            self.mmyear_combo.set_active(0)
        self.mmyear_combo.connect('changed', self.on_mmyear_changed)

        self.available_levels = []
        self.update_available_levels(prefs)

        ListManagerPanel.__init__(self, db, status, prefs, recollections,
                                  self.available_levels,
                                  tr('Available levels'),
                                  mini_items_nb=mini_items_nb,
                                  setup_buttons_icons=False,
                                  editable=[False], enable_buttons=False,
                                  reorderable=False)

        info_label1 = Gtk.Label(self.tr('Select the levels you wish.'))
        self.attach_next_to(info_label1, self.treeview,
                            Gtk.PositionType.BOTTOM, 1, 1)

        self.rightgrid = Gtk.Grid()

        label1 = Gtk.Label()
        text = self.tr('Destination directory:')
        label1.set_markup(f'<span fgcolor="#595959"><b>{text}</b></span>')
        label1.props.margin_right = 10
        self.rightgrid.attach(label1, 0, 0, 1, 1)

        dest_dir = self.recollections.templates_dest_dir
        self.dest_dir = Gtk.Label()
        # self.dest_dir.props.margin_top = 10
        self.dest_dir.set_text(dest_dir)
        self.rightgrid.attach_next_to(self.dest_dir, label1,
                                      Gtk.PositionType.RIGHT, 1, 1)

        self.choosedir_button = Gtk.ToolButton.new()
        self.choosedir_button.set_vexpand(False)
        self.choosedir_button.props.margin_top = 10
        self.choosedir_button.props.margin_left = 10
        self.choosedir_button.connect('clicked', self.on_choosedir_clicked)
        self.choosedir_button.set_margin_bottom(10)
        self.rightgrid.attach_next_to(self.choosedir_button,
                                      self.dest_dir,
                                      Gtk.PositionType.RIGHT, 1, 1)

        label2 = Gtk.Label()
        text = self.tr('Year:')
        label2.set_markup(f'<span fgcolor="#595959"><b>{text}</b></span>')
        label2.props.margin_right = 10
        self.rightgrid.attach_next_to(label2, label1,
                                      Gtk.PositionType.BOTTOM, 1, 1)
        self.rightgrid.attach_next_to(self.mmyear_combo, label2,
                                      Gtk.PositionType.RIGHT, 1, 1)

        self.generate_button = Gtk.ToolButton.new()
        self.generate_button.set_vexpand(False)
        self.generate_button.set_hexpand(False)
        self.generate_button.props.margin = 10
        self.generate_button.connect('clicked', self.on_generate_clicked)
        self.generate_button.set_margin_bottom(10)
        self.rightgrid.attach_next_to(self.generate_button, label2,
                                      Gtk.PositionType.BOTTOM, 1, 1)
        #
        self.attach_next_to(self.rightgrid, self.treeview,
                            Gtk.PositionType.RIGHT, 1, 1)

        self.setup_buttons_icons(ICON_THEME)
        self.set_buttons_sensitivity()

    @property
    def chosen_mmyear(self):
        return mathmaker.available_years()[self.mmyear_combo.get_active()]

    @property
    def templates_dirpath(self):
        return Path(self.dest_dir.get_text())

    def update_available_levels(self, prefs):
        mm_levels = mathmaker.available_levels(self.chosen_mmyear,
                                               use_venv=prefs.use_mm_venv,
                                               venv=prefs.mm_venv)
        user_levels = doc_setup.load()['levels']
        levels_scale = user_levels[1:len(user_levels)]
        self.available_levels = levels_scale[0:len(mm_levels)]

    def on_mmyear_changed(self, *args):
        self.recollections.mm_year = self.chosen_mmyear
        self.update_available_levels(self.prefs)
        self.store.clear()
        for L in self.available_levels:
            self.store.append([L])

    def on_choosedir_clicked(self, *args):
        dialog = FolderSelectDialog(self.db, self.status, self.prefs,
                                    self.recollections, self.parentw)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            path = dialog.get_filename()
            self.dest_dir.set_text(path)
            self.recollections.templates_dest_dir = path
        dialog.destroy()

    def on_generate_clicked(self, *args):
        user_levels = doc_setup.load()['levels']
        levels_scale = user_levels[1:len(user_levels)]
        selected = self.selection.get_selected_rows()[1]
        selection = [self.store[selected[i]][0]
                     for i in range(len(selected))]
        mm_levels = mathmaker.available_levels(self.chosen_mmyear,
                                               use_venv=self.prefs.use_mm_venv,
                                               venv=self.prefs.mm_venv)
        mc_belts_json = {mm: cot
                         for mm, cot in zip(mm_levels, levels_scale)}
        BELTS_JSON.write_text(json.dumps(mc_belts_json))

        selected_mm_levels = [mm_levels[levels_scale.index(s)]
                              for s in selection]
        errors = []
        for mm_level, selected_level in zip(selected_mm_levels, selection):
            failed = mathmaker.create_template(
                mm_level, selected_level, use_venv=self.prefs.use_mm_venv,
                venv=self.prefs.mm_venv, dest_dir=self.templates_dirpath)
            if failed:
                errors.append(selected_level)
        if errors:
            levels_list = ', '.join(errors)
            msg = self.tr('An error has been reported during the creation of '
                          'the templates for these levels: {levels_list}')
            if len(errors) == 1:
                msg = self.tr('An error has been reported during '
                              'the creation of the template for '
                              'this level: {levels_list}')
            msg = msg.format(levels_list=levels_list)
            run_message_dialog(self.tr('Errors'),
                               msg,
                               'dialog-error', self.parentw)
        else:
            # Retrieve possible pictures
            pictures = []
            for f in Path(self.templates_dirpath).glob('*.tex'):
                for line in f.read_text().split('\n'):
                    pictures.extend(re.findall(r"\{([^{]*\.eps)\}", line))
            pictures = set(pictures)
            if pictures:
                mm_config = mathmaker.get_user_config(
                    use_venv=self.prefs.use_mm_venv, venv=self.prefs.mm_venv)
                pics_dir = mm_config['PATHS'].get('OUTPUT_DIR', None)
                if pics_dir:
                    for p in pictures:
                        shutil.copy2(Path.home() / pics_dir / p,
                                     Path(self.templates_dirpath))
            # Build answers files
            for mm_level in selected_mm_levels:
                errorcode = mathmaker.compile_tex_file(
                    mc_belts_json[mm_level], directory=self.templates_dirpath)
                if errorcode:
                    msg = self.tr('An error has been reported during the '
                                  'compilation of the template for this '
                                  'file: {file_name}')
                    msg = msg.format(file_name=f'{mm_level}.tex')
                    run_message_dialog(self.tr('Errors'),
                                       msg,
                                       'dialog-error', self.parentw)
                    return
                else:
                    pdf = Pdf.new()
                    filename = mathmaker.belt_filename(mc_belts_json[mm_level])
                    pdf_name = f'{filename}.pdf'
                    corrected_label = self.tr('CORRECTED')
                    corrected_pdf_name = \
                        f'{filename} {corrected_label}.pdf'
                    with Pdf.open(self.templates_dirpath / pdf_name) as src:
                        pdf.pages.extend(src.pages[-2:])
                    pdf.save(self.templates_dirpath / corrected_pdf_name)
                    pdf.close()
            run_message_dialog(self.tr('Finished!'),
                               self.tr('All templates have been successfully '
                                       'created.'),
                               'dialog-information', self.parentw)

    def buttons_icons(self):
        """Defines icon names and fallback to standard icon name."""
        # Last item of each list is the fallback, hence must be standard
        buttons = {'choosedir_button': ['folder-open'],
                   'generate_button': ['system-run']}
        return buttons

    def buttons_labels(self):
        """Define labels of buttons."""
        buttons = {'choosedir_button': self.tr('Choose'),
                   'generate_button': self.tr('Generate')}
        return buttons

    def set_buttons_sensitivity(self):
        selected = self.selection.get_selected_rows()[1]
        self.generate_button.set_sensitive(selected)
