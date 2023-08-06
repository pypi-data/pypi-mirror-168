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

from shutil import copyfile
from sqlalchemy.sql import false
from sqlalchemy.sql.expression import or_, and_

import gi
try:
    gi.require_version('Gtk', '3.0')
    gi.require_version('Poppler', '0.18')
except ValueError:
    raise
else:
    from gi.repository import Gtk, Poppler, GObject

from cotinga.core.env import REPORT_FILE
from cotinga.core.env import ICON_THEME
from cotinga.core import report
from cotinga.core.tools import file_uri
from cotinga.models import Pupils
from cotinga.gui.core.list_manager import ListManagerBase
from cotinga.core.constants import REPORT_MIN_TABLES
from cotinga.core import doc_setup
from cotinga.gui.dialogs import PreviewDialog, SaveAsFileDialog
from cotinga.gui.dialogs import ReportSetupDialog
from cotinga.gui.core import CLASSES
from cotinga.gui.core import PupilsView, MetaView


class ReportsPanel(ListManagerBase, PupilsView, metaclass=MetaView):

    @GObject.Signal()
    def refresh_title_toolbar(self):
        """Notify that the title and toolbar of the app must be refreshed."""

    def __init__(self, db, status, prefs, recollections, parentw, store):
        self.parentw = parentw
        ListManagerBase.__init__(self, db, status, prefs, recollections,
                                 setup_buttons_icons=False, mini_items_nb=0,
                                 store=store, parentw=parentw)

        self.pupils_nb = 0

        # Treeview and its components
        PupilsView.__init__(self)

        # LATER: remove this code duplication with classes_panel
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.add(self.treeview)
        self.scrollable_treelist.set_vexpand(True)
        self.scrollable_treelist.set_hexpand(False)
        self.scrollable_treelist.set_propagate_natural_height(True)
        self.attach(self.scrollable_treelist, 0, 0, 2, 1)

        info_frame = Gtk.Frame()
        frame_content = Gtk.Grid()
        self.info_pupils_nb = Gtk.Label()
        self.info_pupils_nb.props.margin = 5
        self.info_pupils_nb.props.margin_bottom = 8
        self.info_pupils_dist = Gtk.Label()
        self.info_pupils_dist.props.margin = 5
        self.report_data = []
        self.refresh_info()
        frame_content.attach(self.info_pupils_nb, 0, 0, 1, 1)
        frame_content.attach_next_to(self.info_pupils_dist,
                                     self.info_pupils_nb,
                                     Gtk.PositionType.BOTTOM, 1, 1)
        self.preview_button = Gtk.ToolButton.new()
        self.preview_button.set_vexpand(False)
        self.preview_button.set_halign(Gtk.Align.CENTER)
        self.preview_button.set_valign(Gtk.Align.CENTER)
        self.preview_button.connect('clicked', self.on_preview_clicked)
        frame_content.attach_next_to(self.preview_button,
                                     self.info_pupils_dist,
                                     Gtk.PositionType.BOTTOM, 1, 1)
        self.reportsetup_button = Gtk.ToolButton.new()
        self.reportsetup_button.set_vexpand(False)
        self.reportsetup_button.set_halign(Gtk.Align.CENTER)
        self.reportsetup_button.set_valign(Gtk.Align.CENTER)
        self.reportsetup_button.connect('clicked', self.on_reportsetup_clicked)
        frame_content.attach_next_to(self.reportsetup_button,
                                     self.preview_button,
                                     Gtk.PositionType.BOTTOM, 1, 1)
        info_frame.add(frame_content)
        self.attach_next_to(info_frame, self.scrollable_treelist,
                            Gtk.PositionType.RIGHT, 1, 1)

        # TOP TOOLS (filters)
        self.top_tools = Gtk.Grid()
        self.top_tools.set_hexpand(False)
        self.top_tools.props.margin_bottom = 0
        self.top_tools.props.margin_top = 3

        self.filters_label = Gtk.Label(self.tr('Visible classes:'))
        self.filters_label.set_margin_left(5)
        self.filters_label.set_margin_right(10)
        self.top_tools.attach(self.filters_label, 0, 0, 1, 1)

        # LATER: make displaying no_filter and all_filters buttons be an option
        self.no_filter = Gtk.Button(self.tr('None (no class)'))
        self.no_filter.connect('clicked', self.on_no_filter_button_clicked)
        self.no_filter.set_margin_right(3)
        self.top_tools.attach_next_to(self.no_filter,
                                      self.filters_label,
                                      Gtk.PositionType.RIGHT, 1, 1)

        self.all_filters = Gtk.Button(self.tr('All'))
        self.all_filters.connect('clicked', self.on_all_filters_button_clicked)
        self.all_filters.set_margin_right(3)
        self.top_tools.attach_next_to(self.all_filters,
                                      self.no_filter,
                                      Gtk.PositionType.RIGHT, 1, 1)

        self.filter_buttons = Gtk.Grid()
        self.build_filter_buttons()
        self.top_tools.attach_next_to(self.filter_buttons,
                                      self.all_filters,
                                      Gtk.PositionType.RIGHT, 1, 1)

        self.attach_next_to(self.top_tools, self.scrollable_treelist,
                            Gtk.PositionType.TOP, 1, 1)

        bottomvoid_grid = Gtk.Grid()
        bottomvoid_grid.set_hexpand(True)
        self.attach_next_to(bottomvoid_grid, self.top_tools,
                            Gtk.PositionType.RIGHT, 1, 1)
        self.pdf_report = None
        self.setup_buttons_icons(ICON_THEME)
        self.setup_info_visibility()

    def _adjust_tv_columns(self):
        self.col_incl.set_visible(False)
        self.col_class.set_sort_column_id(2)
        self.col_name.set_sort_column_id(3)
        self.col_ilevel.set_sort_column_id(4)
        self.col_ilevel.set_visible(self.status.show_col_ilevel)
        self.col_alevel.set_sort_column_id(5)

    @property
    def grades_nb(self):
        # TODO: looks like it could be partially factorized with
        # classes_panel.grades_nb()
        all_pupils = self.db.session.query(Pupils).all()
        return max([len(pupil.grades or []) for pupil in all_pupils] or [0])

    def buttons_icons(self):
        """Defines icon names and fallback to standard icon name."""
        # Last item of each list is the fallback, hence must be standard
        buttons = ListManagerBase.buttons_icons(self)
        buttons.update({'preview_button': ['application-pdf',
                                           'document-print-preview']})
        buttons.update({'reportsetup_button': ['gnome-settings',
                                               'preferences-desktop']})
        return buttons

    def buttons_labels(self):
        """Defines icon names and fallback to standard icon name."""
        # Last item of each list is the fallback, hence must be standard
        buttons = ListManagerBase.buttons_labels(self)
        buttons.update({'preview_button': self.tr('Preview')})
        buttons.update({'reportsetup_button': self.tr('Setup')})
        return buttons

    def __build_report_data(self):
        constraints = []
        for classname in self.status.filters:
            constraints.append(Pupils.classnames.contains([classname]))
        if constraints:
            # Making use of Pupils.included is True makes the filtering fail
            pupils = self.db.session.query(Pupils).filter(
                and_(Pupils.included == True, or_(*constraints)))  # noqa
        else:
            pupils = self.db.session.query(Pupils).filter(false())
        report_data = []
        for i, level in enumerate(self.levels):
            n = pupils.filter(Pupils.attained_level == level).count()
            if n:
                if i == len(self.levels) - 1:
                    next_level = level
                else:
                    next_level = self.levels[i + 1]
                pupils_list = pupils.filter(
                    Pupils.attained_level == level).all()
                report_data.append((next_level, n, pupils_list))
        pupils_dist = '\n'.join([self.tr('{level}: {number}')
                                 .format(level=item[0], number=item[1])
                                 for item in report_data])
        return (pupils.count(), pupils_dist, report_data)

    def refresh_info(self):
        self.pupils_nb, pupils_dist, self.report_data = \
            self.__build_report_data()
        self.info_pupils_nb.set_text(
            self.tr('Pupils\' number: {}').format(self.pupils_nb))
        self.info_pupils_dist.set_text(
            self.tr('Next evaluation:') + '\n' + pupils_dist)

    def setup_info_visibility(self):
        if self.pupils_nb:
            self.info_pupils_dist.show()
            self.preview_button.show()
            self.reportsetup_button.show()
        else:
            self.info_pupils_dist.hide()
            self.preview_button.hide()
            self.reportsetup_button.hide()

    def on_grades_cols_changed(self, *args):
        event = args[1]
        if event == 'grade-removed':
            self.remove_grades_column()
        elif event == 'grade-added':
            self.add_grades_column()
        self.refresh_info()
        self.setup_info_visibility()

    def build_filter_buttons(self):
        """Build the filter buttons according to available classes."""
        for btn in self.filter_buttons.get_children():
            self.filter_buttons.remove(btn)
        for classname in self.classes:
            button = Gtk.ToggleButton(classname)
            button.set_margin_right(3)
            button.connect('toggled', self.on_filter_button_toggled)
            if classname in self.status.filters:
                button.set_active(True)
            else:
                button.set_active(False)
            self.filter_buttons.add(button)
        self.filter_buttons.show_all()

    def on_filter_button_toggled(self, widget):
        """Called on any of the filter button clicks"""
        classname = widget.get_label()
        if widget.get_active():
            self.status.filters = \
                list(set(self.status.filters + [classname]))
        else:
            self.status.filters = [label
                                   for label in self.status.filters
                                   if label != classname]
        self.class_filter.refilter()
        self.refresh_info()
        self.setup_info_visibility()

    def on_no_filter_button_clicked(self, widget):
        for btn in self.filter_buttons:
            btn.set_active(False)

    def on_all_filters_button_clicked(self, widget):
        for btn in self.filter_buttons:
            btn.set_active(True)

    def on_reportsetup_clicked(self, widget):
        dialog = ReportSetupDialog(self.db, self.status, self.prefs,
                                   self.recollections, self.parentw)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            reportsetup = doc_setup.load()['report']
            new_title = dialog.title.get_text()
            new_subtitle = dialog.subtitle.get_text()
            new_datefmt = dialog.datefmt.get_text()
            new_colwidth = round(dialog.colwidths.get_value(), 1)
            new_maxtables = dialog.max_tables.get_active() + REPORT_MIN_TABLES
            new_maxrows = int(dialog.max_rows.get_value())
            previous_title = reportsetup['title']
            previous_subtitle = reportsetup['subtitle']
            previous_datefmt = reportsetup['date_fmt']
            previous_colwidth = reportsetup['col_width']
            previous_maxrows = reportsetup['max_rows']
            previous_maxtables = reportsetup['max_tables']
            if any(new != previous
                   for (new, previous) in zip([previous_title,
                                               previous_subtitle,
                                               previous_datefmt,
                                               previous_colwidth,
                                               previous_maxrows,
                                               previous_maxtables],
                                              [new_title,
                                               new_subtitle,
                                               new_datefmt,
                                               new_colwidth,
                                               new_maxrows,
                                               new_maxtables])):
                data = {'report': {'title': new_title,
                                   'subtitle': new_subtitle,
                                   'date_fmt': new_datefmt,
                                   'col_width': new_colwidth,
                                   'max_rows': new_maxrows,
                                   'max_tables': new_maxtables}}
                # print(f'will save={data}')
                doc_setup.save(data)
                self.status.document_modified = True
                self.emit('refresh-title-toolbar')

        dialog.destroy()

    def on_preview_clicked(self, widget):
        pages_nb = report.build(self.report_data)
        report.split(REPORT_FILE)
        dialog = PreviewDialog(self.tr('Report preview'), pages_nb, self.tr,
                               self.parentw)
        response = dialog.run()

        if response == Gtk.ResponseType.YES:  # save as
            save_as_dialog = SaveAsFileDialog(self.db, self.status, self.prefs,
                                              self.recollections, self.parentw,
                                              report=True)
            save_as_response = save_as_dialog.run()
            if save_as_response == Gtk.ResponseType.OK:
                report_name = save_as_dialog.get_filename()
                copyfile(REPORT_FILE, report_name)
            save_as_dialog.destroy()
            dialog.destroy()
            self.on_preview_clicked(widget)

        elif response == Gtk.ResponseType.OK:  # print
            operation = Gtk.PrintOperation()
            operation.connect('begin-print', self.begin_print, None)
            operation.connect('draw-page', self.draw_page, None)
            self.pdf_report = Poppler.Document.new_from_file(
                file_uri(REPORT_FILE))
            print_setup = Gtk.PageSetup()
            print_setup.set_orientation(Gtk.PageOrientation.LANDSCAPE)
            print_setup.set_left_margin(7, Gtk.Unit.MM)
            print_setup.set_right_margin(7, Gtk.Unit.MM)
            print_setup.set_top_margin(7, Gtk.Unit.MM)
            print_setup.set_bottom_margin(7, Gtk.Unit.MM)
            operation.set_default_page_setup(print_setup)
            # print_settings = Gtk.PrintSettings()
            # print_settings.set_orientation(Gtk.PageOrientation.LANDSCAPE)
            # operation.set_print_settings(print_settings)
            print_result = operation.run(Gtk.PrintOperationAction.PRINT_DIALOG,
                                         self.parentw)
            if print_result == Gtk.PrintOperationResult.ERROR:
                message = self.operation.get_error()
                errdialog = Gtk.MessageDialog(self.parentw,
                                              0,
                                              Gtk.MessageType.ERROR,
                                              Gtk.ButtonsType.CLOSE,
                                              message)
                errdialog.run()
                errdialog.destroy()
            dialog.destroy()
            self.on_preview_clicked(widget)

        else:  # close or cancel, whatever
            dialog.destroy()
        report.cleanup(REPORT_FILE)

    def begin_print(self, operation, print_ctx, print_data):
        operation.set_n_pages(self.pdf_report.get_n_pages())

    def draw_page(self, operation, print_ctx, page_num, print_data):
        cr = print_ctx.get_cairo_context()
        page = self.pdf_report.get_page(page_num)
        page.render_for_printing(cr)

    def class_filter_func(self, model, treeiter, data):
        """Test if the class in the row is the one in the filter buttons"""
        return any(cl.strip() in self.status.filters
                   for cl in model[treeiter][CLASSES].split(','))
