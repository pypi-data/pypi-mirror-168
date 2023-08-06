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

import os
from datetime import date

import gi
try:
    gi.require_version('Gtk', '3.0')
    gi.require_version('GdkPixbuf', '2.0')
except ValueError:
    raise
else:
    from gi.repository import Gtk, Gio, GdkPixbuf, GObject


from cotinga.core.env import __myname__, __authors__, VERSION
from cotinga.core.env import GUIDIR, COTINGA_ICON
from cotinga.core import doc_setup, Recollections
from cotinga.core.tools import Listing
from cotinga.gui.core import Sharee
from cotinga.gui.pages import ClassesManagerPage, MergePage
from cotinga.gui.pages.panels import ReportsPanel, WelcomePanel, EmptydocPanel
from cotinga.gui.pages.panels import GeneratePanel
from cotinga.gui.toolbar import MainToolbar
from cotinga.gui.dialogs import PreferencesDialog
from cotinga.models import Pupils

GENERATE_TAB_POS = 2


# TODO: add keyboard shorcuts
# examples: suppr to remove an entry (in any editable list),
# ctrl-O to open file, ctrl-s to save, ctrl-S to save as etc.

# TODO: add tooltips on buttons

class __MetaAppWindowSharee(type(Gtk.ApplicationWindow), type(Sharee)):
    pass


class __MetaAppSharee(type(Gtk.Application), type(Sharee)):
    pass


class AppWindow(Gtk.ApplicationWindow, Sharee,
                metaclass=__MetaAppWindowSharee):
    def __init__(self, db, status, prefs, recollections, *args, **kwargs):
        Sharee.__init__(self, db, status, prefs, recollections)
        super().__init__(*args, **kwargs)

        store_types = [str, bool, str, str, str, str, GObject.TYPE_PYOBJECT]
        self.store = Gtk.ListStore(*store_types)

        self.set_icon_from_file(COTINGA_ICON)
        self.set_border_width(3)

        self.hb = Gtk.HeaderBar()
        self.hb.set_show_close_button(True)
        self.hb.props.title = __myname__.capitalize()
        self.set_titlebar(self.hb)

        with open(os.path.join(GUIDIR, 'app_menu.xml'), 'r') as f:
            menu_xml = f.read()
        menu_xml = menu_xml.replace('LABEL_PREFERENCES',
                                    self.tr('Preferences'))
        menu_xml = menu_xml.replace('LABEL_ABOUT', self.tr('About'))
        menu_xml = menu_xml.replace('LABEL_QUIT', self.tr('Quit'))
        builder = Gtk.Builder.new_from_string(menu_xml, -1)
        menu = builder.get_object('app-menu')

        button = Gtk.MenuButton.new()
        popover = Gtk.Popover.new_from_model(button, menu)
        button.set_popover(popover)

        button.show()
        button = Gtk.MenuButton.new()
        icon = Gtk.Image.new_from_icon_name('open-menu-symbolic',
                                            Gtk.IconSize.BUTTON)
        button.add(icon)
        popover = Gtk.Popover.new_from_model(button, menu)

        button.set_popover(popover)
        self.hb.pack_end(button)

        self.maintoolbar = None
        self.appgrid = None
        self.classes_page = None
        self.reports_page = None
        self.merge_page = None
        self.generate_page = None
        self.notebook = None

        self.maingrid = Gtk.Grid()

        self.build_maintoolbar()
        self.maingrid.attach(self.maintoolbar, 0, 0, 1, 1)

        self.refresh()
        self.add(self.maingrid)

        self.app = kwargs.get('application')
        self.connect('delete-event', self.do_quit)

    def do_quit(self, *args):
        self.app.on_quit(None, None)

    def build_maintoolbar(self, *args):
        self.maintoolbar = MainToolbar(*self.shared, self)
        self.maintoolbar.connect('do-refresh-app-title',
                                 self.refresh_app_title)
        self.maintoolbar.connect('do-refresh', self.refresh)
        self.maintoolbar.set_margin_top(6)

    def refresh_app_title(self, *args):
        title = __myname__.capitalize()
        if self.status.document_name:
            title = self.tr('{doc_title} – {appname}')\
                .format(doc_title=os.path.basename(self.status.document_name),
                        appname=__myname__.capitalize())
        elif self.status.document_loaded:
            title = self.tr('(New document) – {appname}')\
                .format(appname=__myname__.capitalize())
        if self.status.document_modified:
            title += ' *'
        self.hb.props.title = title

    def refresh_title_and_toolbar(self, *args):
        self.refresh_app_title(*args)
        self.maintoolbar.refresh()

    def refresh_merge_panels(self, widget, action, classname, pupils_ids):
        for p in self.merge_page.panels:
            if self.merge_page.panels[p].classname == classname:
                self.merge_page.panels[p].refresh_pupils_list(action,
                                                              pupils_ids)

    def refresh(self, *args):
        if self.appgrid:
            self.maingrid.remove(self.appgrid)
            self.appgrid.destroy()

        self.appgrid = Gtk.Grid()
        self.maintoolbar.refresh()

        if self.db.session is None:
            wp = WelcomePanel(self.tr)
            self.appgrid.attach(wp, 0, 0, 1, 1)
        else:
            classnames = doc_setup.load()['classes']
            if not classnames:
                edp = EmptydocPanel(self.tr)
                self.appgrid.attach(edp, 0, 0, 1, 1)
            else:  # document loaded and there are classnames available
                self.recollections = Recollections()
                self.store.clear()
                for pupil in self.db.session.query(Pupils).all():
                    self.store.append([str(pupil.id), pupil.included,
                                       Listing(pupil.classnames).joined(),
                                       pupil.fullname, pupil.initial_level,
                                       pupil.attained_level,
                                       Listing(pupil.grades)])
                self.classes_page = ClassesManagerPage(self.db, self.status,
                                                       self.prefs,
                                                       self.recollections,
                                                       self, self.store)
                self.classes_page.setup_pages()

                self.reports_page = ReportsPanel(self.db, self.status,
                                                 self.prefs,
                                                 self.recollections, self,
                                                 self.store)
                self.merge_page = MergePage(self.db, self.status, self.prefs,
                                            self.recollections, self)

                self.generate_page = GeneratePanel(self.db, self.status,
                                                   self.prefs,
                                                   self.recollections, self)

                for p in self.classes_page.panels:
                    self.reports_page.connect('refresh-title-toolbar',
                                              self.refresh_title_and_toolbar)
                    self.classes_page.panels[p]\
                        .connect('refresh-title-toolbar',
                                 self.refresh_title_and_toolbar)
                    self.classes_page.panels[p]\
                        .connect('pupils-list-changed',
                                 self.refresh_merge_panels)
                    self.classes_page.panels[p]\
                        .connect('grades-columns-changed',
                                 self.reports_page.on_grades_cols_changed)

                for p in self.merge_page.panels:
                    self.merge_page.panels[p]\
                        .connect('data-reordered',
                                 self.refresh_title_and_toolbar)

                if self.notebook:
                    self.notebook.destroy()
                self.notebook = Gtk.Notebook()

                self.notebook.append_page(self.classes_page,
                                          Gtk.Label(self.tr('Classes')))
                self.notebook.append_page(self.reports_page,
                                          Gtk.Label(self.tr('Reports')))
                self.notebook.append_page(self.merge_page,
                                          Gtk.Label(self.tr('Merging')))
                if self.prefs.show_generate_panel:
                    self.notebook.insert_page(self.generate_page,
                                              Gtk.Label(self.tr('Generate')),
                                              GENERATE_TAB_POS)
                self.appgrid.attach(self.notebook, 0, 0, 1, 1)

        self.maingrid.attach_next_to(self.appgrid, self.maintoolbar,
                                     Gtk.PositionType.BOTTOM, 1, 1)
        self.refresh_app_title()
        self.show_all()


class Application(Gtk.Application, Sharee, metaclass=__MetaAppSharee):
    def __init__(self, db, status, prefs, recollections, *args, **kwargs):
        Sharee.__init__(self, db, status, prefs, recollections)
        super().__init__(*args, application_id='org.cotinga_app', **kwargs)
        self.window = None
        self.logo = GdkPixbuf.Pixbuf.new_from_file_at_scale(COTINGA_ICON,
                                                            128, -1, True)

    def do_startup(self):
        Gtk.Application.do_startup(self)

        action = Gio.SimpleAction.new('preferences', None)
        action.connect('activate', self.on_preferences)
        self.add_action(action)

        action = Gio.SimpleAction.new('about', None)
        action.connect('activate', self.on_about)
        self.add_action(action)

        action = Gio.SimpleAction.new('quit', None)
        action.connect('activate', self.on_quit)
        self.add_action(action)
        if self.window:
            self.window.refresh()

    def do_activate(self):
        # We only allow a single window and raise any existing ones
        if not self.window:
            # Windows are associated with the application
            # when the last one is closed the application shuts down
            self.window = AppWindow(*self.shared, application=self,
                                    title=__myname__.capitalize())
        # self.window.set_size_request(400, 250)
        self.window.set_default_size(600, 400)
        self.window.present()
        self.window.show_all()
        self.window.refresh()

    def on_preferences(self, action, param):
        pref_dialog = PreferencesDialog(self.tr('Preferences'),
                                        self.prefs.language,
                                        self.tr,
                                        self.prefs)
        pref_dialog.set_transient_for(self.window)
        pref_dialog.set_modal(True)
        pref_dialog.run()
        chosen_language = pref_dialog.chosen_language
        chosen_devtools = pref_dialog.devtools_switch.get_active()
        chosen_show_toolbar_labels = pref_dialog\
            .show_toolbar_labels_switch.get_active()
        self.prefs.show_generate_panel = pref_dialog.enable_generate_panel
        self.prefs.mm_venv = pref_dialog.mmvenv_path
        self.prefs.use_mm_venv = pref_dialog.use_mmvenv
        pref_dialog.destroy()
        if (hasattr(self.window, 'notebook') and self.window.notebook
           and self.window.notebook.get_n_pages()):
            generate_title = self.tr('Generate')
            nb = self.window.notebook
            nth_title = nb.get_tab_label_text(
                nb.get_nth_page(GENERATE_TAB_POS))
            if self.prefs.show_generate_panel:
                # it's time to show it (if not yet)
                if nth_title != generate_title:
                    nb.insert_page(self.window.generate_page,
                                   Gtk.Label(generate_title),
                                   GENERATE_TAB_POS)
            else:  # hide it!
                if nth_title == generate_title:
                    nb.remove_page(GENERATE_TAB_POS)
        previous_language = self.prefs.language
        previous_devtools = self.prefs.enable_devtools
        previous_show_toolbar_labels = self.prefs.show_toolbar_labels
        recreate_window = False
        if (chosen_language is not None
                and previous_language != chosen_language):
            self.prefs.language = chosen_language
            recreate_window = True
        if previous_devtools != chosen_devtools:
            self.prefs.enable_devtools = chosen_devtools
            recreate_window = True
        if previous_show_toolbar_labels != chosen_show_toolbar_labels:
            self.prefs.show_toolbar_labels = chosen_show_toolbar_labels
            recreate_window = True
        if recreate_window:
            self.window.destroy()
            self.window = None
            self.do_activate()

    def on_about(self, action, param):
        about_dialog = Gtk.AboutDialog(transient_for=self.window, modal=True)
        about_dialog.set_authors(__authors__)
        about_dialog.set_version(VERSION)
        about_dialog.set_program_name(__myname__)
        # about_dialog.props.wrap_license = True
        about_dialog.set_website(
            'https://gitlab.com/nicolas.hainaux/cotinga')
        about_dialog.set_website_label(self.tr('Cotinga website'))
        about_dialog.set_logo(self.logo)
        current_year = f'{date.today().strftime("%Y")}'
        about_dialog.set_copyright(
            f'Copyright © 2018-{current_year} Nicolas Hainaux')
        about_dialog.set_comments(self.tr('Cotinga helps teachers to manage '
                                          "their pupils' progression."))
        # with open('LICENSE', 'r') as f:  # Either this or the licence type
        #     about_dialog.set_license(f.read())
        about_dialog.set_license_type(Gtk.License.GPL_3_0)

        about_dialog.run()
        about_dialog.destroy()

    def on_quit(self, action, param):
        self.quit()
