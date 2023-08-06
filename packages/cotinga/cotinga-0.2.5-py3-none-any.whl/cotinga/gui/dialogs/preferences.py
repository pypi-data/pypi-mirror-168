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

from babel import Locale
import gi
try:
    gi.require_version('Gtk', '3.0')
    gi.require_version('GdkPixbuf', '2.0')
except ValueError:
    raise
else:
    from gi.repository import Gtk, GdkPixbuf

from cotinga.core.env import SUPPORTED_LANGUAGES, FLAGSDIR
from cotinga.core import mathmaker
from cotinga.core.env import ICON_THEME
from cotinga.gui.core import IconsThemable

__all__ = ['PreferencesDialog']


class __MetaDialog(type(Gtk.Dialog), type(IconsThemable)):
    pass


class PreferencesDialog(Gtk.Dialog, IconsThemable, metaclass=__MetaDialog):

    def __init__(self, title, default_language, tr, prefs, parentw=None,
                 first_run=False):
        self.tr = tr
        if parentw is None:
            parentw = Gtk.ApplicationWindow()
        self.parentw = parentw
        self.prefs = prefs
        buttons = {True: (Gtk.STOCK_OK, Gtk.ResponseType.OK),
                   False: (Gtk.STOCK_CLOSE, Gtk.ResponseType.CLOSE)}
        Gtk.Dialog.__init__(self, title, parentw, 0, buttons[first_run])

        self.set_default_size(250, 100)
        self.box = self.get_content_area()
        # As Gtk.Box will get deprecated, one can expect that
        # get_content_area() will later return something else than a Box.
        # Note that then, box can be replaced by self.page1

        self.page1 = Gtk.Grid()

        if first_run:
            self.setup_page1_language(default_language)
            self.box.add(self.page1)
        else:
            self.notebook = Gtk.Notebook()
            self.setup_page1(default_language)
            self.availability = Gtk.Grid()
            self.mm_availability_label = Gtk.Label()
            self.mm_availability_icon = Gtk.Image()
            self.use_mmvenv = self.prefs.use_mm_venv
            self.mmvenv_checkbutton = Gtk.CheckButton(
                label=self.tr('Use a virtual environment for mathmaker'))
            self.mmvenv_checkbutton.connect('toggled',
                                            self.on_use_venv_toggled)
            self.mmvenv_line2 = Gtk.Grid()
            self.mmvenv_path = self.prefs.mm_venv
            self.mmvenv_path_label = Gtk.Label()
            self.choosevenv_button = Gtk.ToolButton.new()
            self.panel_enabling = Gtk.Grid()
            self.panel_enabling.set_column_spacing(10)
            self.enable_generate_panel = self.prefs.show_generate_panel
            self.page2 = Gtk.Grid()
            self.setup_page2()
            self.notebook.append_page(self.page1,
                                      Gtk.Label(self.tr('General')))
            self.notebook.append_page(self.page2,
                                      Gtk.Label(self.tr('Automatic tests '
                                                        'generation')))

            self.buttons = {'choosevenv_button': self.choosevenv_button}
            self.setup_buttons_icons(ICON_THEME)
            self.mmvenv_checkbutton.set_active(self.use_mmvenv)
            self.box.add(self.notebook)

        self.show_all()
        if not first_run:
            self.refresh_page2()

    def setup_page_layout(self, n):
        nth_page = getattr(self, f'page{n}')
        nth_page.set_border_width(25)
        nth_page.set_column_spacing(25)
        nth_page.set_row_spacing(15)

    def setup_page1_language(self, default_language):
        self.setup_page_layout(1)

        self.language_label = Gtk.Label(self.tr('Choose a language:'))
        self.page1.attach(self.language_label, 0, 0, 1, 1)

        store = Gtk.ListStore(GdkPixbuf.Pixbuf, str)
        self.languages = {}
        currently_selected = -1
        for i, lang_code in enumerate(SUPPORTED_LANGUAGES):
            loc = Locale.parse(lang_code)
            language_name = loc.get_display_name(default_language)
            flag_filename = '{}.svg'.format(lang_code.split('_')[1])
            flag_icon = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                str(FLAGSDIR / flag_filename), 24, -1, True)
            store.append([flag_icon, language_name])
            self.languages[language_name] = lang_code
            if lang_code == default_language:
                currently_selected = i

        self.combo = Gtk.ComboBox.new_with_model(store)

        renderer = Gtk.CellRendererPixbuf()
        self.combo.pack_start(renderer, True)
        self.combo.add_attribute(renderer, 'pixbuf', 0)

        renderer = Gtk.CellRendererText()
        self.combo.pack_start(renderer, False)
        self.combo.add_attribute(renderer, 'text', 1)

        if currently_selected >= 0:
            self.combo.set_active(currently_selected)
        self.combo.connect('changed', self.on_language_changed)

        self.chosen_language = None

        self.page1.attach_next_to(self.combo, self.language_label,
                                  Gtk.PositionType.BOTTOM, 1, 1)

    def setup_page1(self, default_language):
        self.setup_page1_language(default_language)

        show_toolbar_labels = Gtk.Label(self.tr('Show toolbar buttons labels'))
        show_toolbar_labels.props.margin_right = 10
        self.show_toolbar_labels_switch = Gtk.Switch()
        self.show_toolbar_labels_switch.set_active(
            self.prefs.show_toolbar_labels)

        self.page1.attach_next_to(show_toolbar_labels, self.language_label,
                                  Gtk.PositionType.RIGHT, 1, 1)
        self.page1.attach_next_to(self.show_toolbar_labels_switch,
                                  self.combo,
                                  Gtk.PositionType.RIGHT, 1, 1)

        devtools_label = Gtk.Label(self.tr('Developer tools'))
        devtools_label.props.margin_right = 10
        self.devtools_switch = Gtk.Switch()
        self.devtools_switch.set_active(self.prefs.enable_devtools)

        self.page1.attach_next_to(devtools_label, show_toolbar_labels,
                                  Gtk.PositionType.RIGHT, 1, 1)
        self.page1.attach_next_to(self.devtools_switch,
                                  self.show_toolbar_labels_switch,
                                  Gtk.PositionType.RIGHT, 1, 1)

    def setup_page2(self):
        self.setup_page_layout(2)

        # attach mathmaker's availability line (will be refreshed later)
        self.availability.set_column_spacing(10)
        self.availability.attach(self.mm_availability_icon, 0, 0, 1, 1)
        self.availability.attach_next_to(self.mm_availability_label,
                                         self.mm_availability_icon,
                                         Gtk.PositionType.RIGHT, 1, 1)
        self.page2.attach(self.availability, 0, 0, 1, 1)

        # mathmaker's optional venv line
        self.page2.attach_next_to(self.mmvenv_checkbutton, self.availability,
                                  Gtk.PositionType.BOTTOM, 1, 1)
        self.choosevenv_button.set_vexpand(False)
        self.choosevenv_button.props.margin = 10
        self.choosevenv_button.connect('clicked', self.on_choosevenv_clicked)
        self.mmvenv_line2.set_column_spacing(10)
        self.mmvenv_line2.attach(self.choosevenv_button, 0, 0, 1, 1)
        self.mmvenv_path_label.set_label(self.prefs.mm_venv)
        self.mmvenv_line2.attach_next_to(self.mmvenv_path_label,
                                         self.choosevenv_button,
                                         Gtk.PositionType.RIGHT, 1, 1)
        self.page2.attach_next_to(self.mmvenv_line2, self.mmvenv_checkbutton,
                                  Gtk.PositionType.BOTTOM, 1, 1)

        # generate panel switch
        mm_label = Gtk.Label(self.tr('Enable tests generation panel'))
        self.panel_enabling.attach(mm_label, 0, 0, 1, 1)
        self.mm_panel_switch = Gtk.Switch()
        self.mm_panel_switch.set_active(self.prefs.show_generate_panel)
        self.mm_panel_switch.connect('notify::active',
                                     self.on_mm_panel_switch_toggled)
        self.panel_enabling.attach_next_to(self.mm_panel_switch, mm_label,
                                           Gtk.PositionType.RIGHT, 1, 1)
        self.page2.attach_next_to(self.panel_enabling, self.mmvenv_line2,
                                  Gtk.PositionType.BOTTOM, 1, 1)

    def refresh_mm_availability(self):
        labels = {True: self.tr('mathmaker is available'),
                  False: self.tr('mathmaker is not available')}
        icons = {True: ['emblem-default', Gtk.IconSize.LARGE_TOOLBAR],
                 False: ['emblem-unreadable', Gtk.IconSize.LARGE_TOOLBAR]}
        colors = {True: '#5DAE49', False: '#DC322F'}
        availability = mathmaker.is_available(self.use_mmvenv,
                                              self.mmvenv_path)
        # print(f'check mm venv={self.mmvenv_path}')
        # print(f'availability={availability}')
        text = labels[availability]
        color = colors[availability]
        self.mm_availability_label.set_markup(
            f'<span fgcolor="{color}"><b>{text}</b></span>')
        self.mm_availability_icon.set_from_icon_name(*icons[availability])
        return availability

    def refresh_page2(self):
        mm_available = self.refresh_mm_availability()
        if self.mmvenv_checkbutton.get_active():
            self.mmvenv_line2.show_all()
        else:
            self.mmvenv_line2.hide()
        if mm_available:
            self.panel_enabling.show_all()
        else:
            self.panel_enabling.hide()

    def on_language_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            language_name = model[tree_iter][1]
            print('Selected: language_name={}, country_code={}'
                  .format(language_name, self.languages[language_name]))
            self.chosen_language = self.languages[language_name]
        else:
            entry = combo.get_child()
            print('Entered: %s' % entry.get_text())

    def on_use_venv_toggled(self, *args):
        self.use_mmvenv = self.mmvenv_checkbutton.get_active()
        self.refresh_page2()

    def on_mm_panel_switch_toggled(self, switch, *args):
        self.enable_generate_panel = self.mm_panel_switch.get_active()

    def on_choosevenv_clicked(self, *args):
        folder_select_dialog = \
            Gtk.FileChooserDialog(
                self.tr('Please select a folder'), self.parentw,
                Gtk.FileChooserAction.SELECT_FOLDER,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        response = folder_select_dialog.run()
        if response == Gtk.ResponseType.OK:
            self.mmvenv_path = folder_select_dialog.get_filename()
            self.mmvenv_path_label.set_label(self.mmvenv_path)
        folder_select_dialog.destroy()

        self.refresh_page2()

    def buttons_icons(self):
        """Define icon names and fallback to standard icon name."""
        # Last item of each list is the fallback, hence must be standard
        buttons = {'choosevenv_button': ['folder-open']
                   }
        return buttons

    def buttons_labels(self):
        """Define labels of buttons."""
        buttons = {'choosevenv_button': self.tr('Choose'),
                   }
        return buttons
