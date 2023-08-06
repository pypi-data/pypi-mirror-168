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
    from gi.repository import Gtk, GLib, GObject

import threading
from pathlib import Path
from datetime import date
from gettext import translation

from sqlalchemy.sql.expression import and_

from cotinga.gui.dialogs import run_message_dialog
from cotinga.core.merge_tex import tex_compiler_is_not_available
from cotinga.core.merge_tex import list_levels
from cotinga.core.merge_tex import missing_templates
from cotinga.core.merge_tex import incorrect_templates
from cotinga.core.merge_tex import MergingOperation
from cotinga.core.merge_tex import check_templates_fmt
from cotinga.core.env import ICON_THEME, COTINGA_ICON
from cotinga.core.errors import MixedTemplatesFormatsError
from cotinga.core.errors import NoTemplateFoundError
from cotinga.gui.core.list_manager import ListManagerPanel
from cotinga.gui.dialogs import FolderSelectDialog
from cotinga.core.env import LOCALEDIR, L10N_DOMAIN
from cotinga.models import Pupils
from cotinga.gui.core import ID
from cotinga.core.presets import default_tests_title


class MergePanel(ListManagerPanel):

    @GObject.Signal
    def data_reordered(self):
        """Notify that the order of pupils has changed."""

    def __init__(self, db, status, prefs, recollections, parentw, classname,
                 mini_items_nb=2):
        self.lock_on_rows_reordered = False
        self.parentw = parentw
        self.classname = classname
        self.db = db
        self.recollections = recollections
        pupils_list = self.init_pupils_list()

        tr = translation(L10N_DOMAIN, LOCALEDIR, [prefs.language]).gettext

        ListManagerPanel.__init__(self, db, status, prefs, recollections,
                                  pupils_list,
                                  ['id',
                                   tr('Distribution order for {classname}')
                                   .format(classname=classname)],
                                  store_types=[int, str],
                                  visible_cols=[False, True],
                                  mini_items_nb=mini_items_nb,
                                  setup_buttons_icons=False,
                                  editable=[False, False],
                                  enable_buttons=False)

        # The 'rows-reordered' signal is not emitted when using drag and
        # drop, because an insertion followed by a removal is used in that
        # case.
        # When the 'row-inserted' signal is emitted, the row is most of the
        # time still empty. It may be used to know the destination row.
        # The 'row-deleted' finishes the drag and drop operation, hence can be
        # used to detect a reordering.
        self.current_ids = pupils_list
        self.store.connect('row-deleted', self.on_rows_reordered)

        self.rightgrid = Gtk.Grid()

        info_label1 = Gtk.Label(self.tr('Drag and drop to change order.'))
        self.attach_next_to(info_label1, self.treeview,
                            Gtk.PositionType.BOTTOM, 1, 1)

        info_label2 = Gtk.Label(
            self.tr('Only included pupils of {classname} will show up here.')
            .format(classname=classname))
        self.attach_next_to(info_label2, info_label1,
                            Gtk.PositionType.BOTTOM, 1, 1)

        info_label3 = Gtk.Label(
            self.tr('Newly added pupils will be appended to this list.'))
        self.attach_next_to(info_label3, info_label2,
                            Gtk.PositionType.BOTTOM, 1, 1)

        label1 = Gtk.Label()
        text = self.tr("Templates' directory:")
        label1.set_markup(f'<span fgcolor="#595959"><b>{text}</b></span>')
        label1.props.margin_right = 10
        self.rightgrid.attach(label1, 0, 0, 1, 1)

        templates_dir = \
            self.recollections.templates_paths.get(classname, str(Path.home()))
        self.templates_dir = Gtk.Label()
        # self.templates_dir.set_editable(False)
        # self.templates_dir.props.margin_top = 10
        self.templates_dir.set_text(templates_dir)
        self.rightgrid.attach_next_to(self.templates_dir, label1,
                                      Gtk.PositionType.RIGHT, 1, 1)

        self.choosedir_button = Gtk.ToolButton.new()
        self.choosedir_button.set_vexpand(False)
        self.choosedir_button.props.margin_top = 10
        self.choosedir_button.props.margin_left = 10
        self.choosedir_button.connect('clicked', self.on_choosedir_clicked)
        self.choosedir_button.set_margin_bottom(10)
        self.rightgrid.attach_next_to(self.choosedir_button,
                                      self.templates_dir,
                                      Gtk.PositionType.RIGHT, 1, 1)

        label2 = Gtk.Label()
        text = self.tr('Test name:')
        label2.set_markup(f'<span fgcolor="#595959"><b>{text}</b></span>')
        label2.props.margin_top = 10
        label2.props.margin_right = 10
        self.rightgrid.attach_next_to(label2, label1,
                                      Gtk.PositionType.BOTTOM, 1, 1)
        self.test_name = Gtk.Entry()
        self.test_name.set_editable(True)
        self.test_name.props.margin_top = 10
        self.test_name.set_text(f'{str(date.today())}_{classname}')
        self.rightgrid.attach_next_to(self.test_name, self.templates_dir,
                                      Gtk.PositionType.BOTTOM, 2, 1)

        label3 = Gtk.Label()
        text = self.tr('Title:')
        label3.set_markup(f'<span fgcolor="#595959"><b>{text}</b></span>')
        label3.props.margin_top = 10
        label3.props.margin_right = 10
        self.rightgrid.attach_next_to(label3, label2,
                                      Gtk.PositionType.BOTTOM, 1, 1)
        self.test_title = Gtk.Entry()
        self.test_title.set_editable(True)
        self.test_title.props.margin_top = 10
        self.test_title.set_text(f'{default_tests_title()}')
        self.rightgrid.attach_next_to(self.test_title, label3,
                                      Gtk.PositionType.RIGHT, 2, 1)

        label4 = Gtk.Label()
        text = self.tr(r'Process &lt;BELT&gt; tag:')
        label4.set_markup(f'<span fgcolor="#595959"><b>{text}</b></span>')
        label4.props.margin_top = 10
        label4.props.margin_right = 10
        label4.props.margin_left = 10
        self.rightgrid.attach_next_to(label4, label3,
                                      Gtk.PositionType.BOTTOM, 1, 1)

        self.process_belt_tag = self.recollections.process_belt_tag\
            .get(self.classname, 'none')
        radiogrid = Gtk.Grid()
        radiogrid.props.margin_top = 10

        radio1 = Gtk.RadioButton.new_from_widget(None)
        radio1.set_label(self.tr('None (no processing)'))
        radio1.connect('toggled', self.on_radio_toggled, 'none')
        radiogrid.attach(radio1, 0, 0, 1, 1)
        radio1.set_active(True)

        radio2 = Gtk.RadioButton.new_from_widget(radio1)
        radio2.set_label(self.tr('lower case'))
        radio2.connect('toggled', self.on_radio_toggled, 'lower')
        radiogrid.attach_next_to(radio2, radio1, Gtk.PositionType.RIGHT, 1, 1)
        radio2.set_active(self.process_belt_tag == 'lower')

        radio3 = Gtk.RadioButton.new_from_widget(radio1)
        radio3.set_label(self.tr('Capitalize first word'))
        radio3.connect('toggled', self.on_radio_toggled, 'capitalize')
        radiogrid.attach_next_to(radio3, radio2, Gtk.PositionType.RIGHT, 1, 1)
        radio3.set_active(self.process_belt_tag == 'capitalize')

        radio4 = Gtk.RadioButton.new_from_widget(radio1)
        radio4.set_label(self.tr('Capitalize All Words'))
        radio4.connect('toggled', self.on_radio_toggled, 'title')
        radiogrid.attach_next_to(radio4, radio3, Gtk.PositionType.RIGHT, 1, 1)
        radio4.set_active(self.process_belt_tag == 'title')

        self.rightgrid.attach_next_to(radiogrid, label4,
                                      Gtk.PositionType.RIGHT, 4, 1)

        self.merge_button = Gtk.ToolButton.new()
        self.merge_button.set_vexpand(False)
        self.merge_button.set_hexpand(False)
        self.merge_button.props.margin = 10
        self.merge_button.connect('clicked', self.on_merge_clicked)
        self.merge_button.set_margin_bottom(10)
        self.rightgrid.attach_next_to(self.merge_button, label4,
                                      Gtk.PositionType.BOTTOM, 1, 1)

        self.attach_next_to(self.rightgrid, self.treeview,
                            Gtk.PositionType.RIGHT, 1, 1)

        self.setup_buttons_icons(ICON_THEME)
        # self.show_all()

    def get_id_fullname_pairs(self, pupils_ids):
        return [(i, self.db.session.query(Pupils)
                .filter(Pupils.id == i).all()[0].fullname)
                for i in pupils_ids]

    def init_pupils_list(self):
        # only pupils ids are stored in recollections
        pupils_ids = self.recollections.merge_orders.get(self.classname, [])
        pupils_list = self.get_id_fullname_pairs(pupils_ids)
        if pupils_list:
            return pupils_list
        else:
            # Making use of "Pupils.included is True" makes the filtering fail
            db_pupils = self.db.session.query(Pupils).filter(
                and_(Pupils.included == True,  # noqa
                     Pupils.classnames.contains([self.classname])))\
                .order_by(Pupils.fullname).all()
            db_pupils = [(p.id, p.fullname) for p in db_pupils]
            return db_pupils

    def refresh_pupils_list(self, action, pupils_ids):
        pupils_ids = [int(i) for i in pupils_ids.split(', ')]
        if action in ['remove', 'exclude']:
            to_remove = []
            for row in self.store:
                if row[ID] in pupils_ids:
                    to_remove.append(row)
            for row in to_remove:
                self.store.remove(row.iter)

        elif action in ['add', 'include']:
            for data in self.get_id_fullname_pairs(pupils_ids):
                self.store.append(data)

        elif action == 'rename':
            i = pupils_ids[0]
            for row in self.store:
                if row[ID] == i:
                    _, row[1] = self.get_id_fullname_pairs(pupils_ids)[0]

        self.recollections.merge_orders = (self.classname,
                                           [p[ID] for p in self.store])

    @property
    def pupils_fullnames(self):
        return [row[1] for row in self.store if row[1] is not None]

    @property
    def pupils_ids(self):
        return [row[ID] for row in self.store if row[ID] is not None]

    @property
    def templates_dirpath(self):
        return Path(self.templates_dir.get_text())

    def on_choosedir_clicked(self, *args):
        dialog = FolderSelectDialog(self.db, self.status, self.prefs,
                                    self.recollections, self.parentw)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            path = dialog.get_filename()
            self.templates_dir.set_text(path)
            self.recollections.templates_paths = (self.classname, path)
        dialog.destroy()

    def on_rows_reordered(self, *args):
        if not self.lock_on_rows_reordered:
            if self.current_ids != self.pupils_ids:
                self.status.document_modified = True
                self.current_ids = self.pupils_ids
                self.recollections.merge_orders = (self.classname,
                                                   self.current_ids)
                self.emit('data-reordered')

    def on_radio_toggled(self, button, action):
        if button.get_active():
            self.process_belt_tag = action
            self.recollections.process_belt_tag = (self.classname, action)

    def on_merge_clicked(self, *args):
        levels = list_levels(self.classname, self.pupils_fullnames, self.db)
        try:
            fmt = check_templates_fmt(self.templates_dirpath, levels)
        except MixedTemplatesFormatsError:
            run_message_dialog(self.tr('Mixed templates'),
                               self.tr('Found single AND paired templates in '
                                       'the templates directory. You can '
                                       'either use one single template per '
                                       'level (named after the level: '
                                       'levelname.tex), or a pair of '
                                       'templates (e.g. levelname0.tex '
                                       'and levelname1.tex).'),
                               'dialog-error', self.parentw)
            return
        except NoTemplateFoundError:
            run_message_dialog(self.tr('No templates found'),
                               self.tr('Could not find any template in the '
                                       'templates\' directory.'),
                               'dialog-error', self.parentw)
            return
        missing = missing_templates(self.templates_dirpath, levels, fmt)
        incorrect = []
        # TODO: also check that rights are OK to create the tests_dir
        # directory and write files to it
        tests_dir = self.templates_dirpath / self.test_name.get_text()
        if not missing:
            incorrect = incorrect_templates(self.templates_dirpath, levels,
                                            fmt)
        if tex_compiler_is_not_available():
            run_message_dialog(self.tr('No compiler'),
                               self.tr('No compiler seems to be installed.'),
                               'dialog-error', self.parentw)
            return
        elif missing:
            run_message_dialog(self.tr('Missing templates'),
                               self.tr('Following templates are missing: '
                                       f"{', '.join(m for m in missing)}"),
                               'dialog-error', self.parentw)
            return
        elif incorrect:
            msg = self.tr('Following templates miss a <FULLNAME> placeholder: '
                          '{missing}')
            msg = msg.format(missing=missing)
            run_message_dialog(self.tr('Incorrect templates'), msg,
                               'dialog-error', self.parentw)
            return
        elif tests_dir.exists():
            run_message_dialog(self.tr('Tests directory already exists'),
                               self.tr('Tests directory already exists.\n'
                                       'Please delete it or change its name\n'
                                       'in order to have a clean place\nto '
                                       'compile the documents.'),
                               'dialog-error', self.parentw)
            return

        # No errors, the merging may begin
        args = (self.templates_dirpath, self.test_name.get_text(),
                self.classname, self.pupils_fullnames, levels, fmt)
        window = ProgressBarWindow(self.tr, self.parentw, *args)
        window.set_modal(True)
        window.set_default_size(400, 100)
        window.set_decorated(False)
        window.merging.title = self.test_title.get_text()
        window.merging.process_belt_tag = self.process_belt_tag
        window.present()
        window.show_all()
        window.start_merging()

    def buttons_icons(self):
        """Defines icon names and fallback to standard icon name."""
        # Last item of each list is the fallback, hence must be standard
        buttons = {'choosedir_button': ['folder-open'],
                   'merge_button': ['system-run']}
        return buttons

    def buttons_labels(self):
        """Define labels of buttons."""
        buttons = {'choosedir_button': self.tr('Choose'),
                   'merge_button': self.tr('Merge')}
        return buttons


class ProgressBarWindow(Gtk.Window):

    def __init__(self, tr, parentw, templates_dirpath, test_name, classname,
                 pupils_fullnames, levels, fmt, *args, **kwargs):
        self.tr = tr
        self.parentw = parentw
        self.templates_dirpath = templates_dirpath
        self.test_name = test_name
        self.classname = classname
        self.pupils_fullnames = pupils_fullnames
        self.levels = levels
        self.fmt = fmt
        self.merged_name = self.tr('TEST') \
            + f'_{self.classname}_{str(date.today())}.pdf'

        self.merging = MergingOperation(self.tr)
        self.merging.connect('merging-finished', self.on_merging_finished)
        self.merging.connect('merging-aborted', self.on_merging_aborted)

        super().__init__(*args, **kwargs)

        self.state_icon = Gtk.Image()

        self.content = Gtk.Grid()
        self.info_label = Gtk.Label(self.tr('Compilation'))
        self.info_label.props.margin = 5
        self.info_label.set_line_wrap(True)
        self.info_label.set_justify(Gtk.Justification.CENTER)
        self.progress_bar = Gtk.ProgressBar()
        self.progress_bar.props.margin = 5
        self.progress_bar.set_size_request(396, 8)
        self.ok_button = Gtk.Button.new_with_label(self.tr('OK'))
        self.ok_button.set_sensitive(False)
        self.ok_button.connect('clicked', self.on_ok_clicked)

        self.content.attach(self.info_label, 0, 0, 3, 3)
        self.content.attach(self.progress_bar, 0, 3, 3, 1)
        self.content.attach(self.ok_button, 1, 4, 1, 1)
        # self.content.attach_next_to(self.progress_bar, self.info_label,
        #                             Gtk.PositionType.BOTTOM, 2, 3)
        # self.content.attach_next_to(self.ok_button, self.progress_bar,
        #                             Gtk.PositionType.BOTTOM, 1, 1)
        self.add(self.content)
        self.set_icon_from_file(COTINGA_ICON)
        self.set_title(self.tr('Compilation'))
        self.set_keep_above(True)

    def start_merging(self):
        args = (self.templates_dirpath, self.test_name,
                self.classname, self.pupils_fullnames, self.levels, self.fmt,
                self.info_label, self.progress_bar, self.merged_name)
        thread = threading.Thread(target=self.merging.merge_tests,
                                  args=args)
        thread.daemon = True
        thread.start()

    def _handle_signal_from_external_thread(self, title, msg, state):
        # See:
        # What if I need to call GTK code in signal handlers emitted from a
        # thread?
        # https://pygobject.readthedocs.io/en/latest/guide/threading.html
        # #threads-faq
        def set_label_from_external_thread(event, result, title, msg, state):
            result.append(self.set_title(title))
            result.append(self.info_label.set_text(msg))
            result.append(self.ok_button.set_sensitive(True))
            result.append(self.state_icon.set_from_icon_name(*state))
            result.append(self.content.attach_next_to(self.state_icon,
                                                      self.ok_button,
                                                      Gtk.PositionType.LEFT,
                                                      1, 1))
            result.append(self.content.show_all())
            event.set()

        event = threading.Event()
        result = []
        GLib.idle_add(set_label_from_external_thread, event, result,
                      title, msg, state)
        event.wait()

    def on_merging_finished(self, *args):
        msg = self.tr('All documents have been sucessfully '
                      'compiled and merged as {output}.')
        msg = msg.format(output=self.merged_name)
        title = self.tr('Finished!')
        state = ['emblem-default', Gtk.IconSize.LARGE_TOOLBAR]
        self._handle_signal_from_external_thread(title, msg, state)

    def on_merging_aborted(self, *args):
        msg = self.tr('Document {doc_name}\ncould not be '
                      'compiled correctly.\nPlease check and '
                      'fix the problem\nbefore trying to '
                      'compile and merge.')
        msg = msg.format(doc_name=self.merging.filename)
        title = self.tr('Compilation failed')
        state = ['emblem-unreadable', Gtk.IconSize.LARGE_TOOLBAR]
        self._handle_signal_from_external_thread(title, msg, state)

    def on_ok_clicked(self, *args):
        self.close()
