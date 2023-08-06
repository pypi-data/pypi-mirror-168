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

import threading

import gi
try:
    gi.require_version('Gtk', '3.0')
except ValueError:
    raise
else:
    from gi.repository import Gtk, GLib

from cotinga.core.env import COTINGA_ICON


class ProgressBarWindow(Gtk.Window):

    def __init__(self, tr, parentw, title, operation_cls, run_args,
                 finished_msg, aborted_msg, *args, finished_title=None,
                 aborted_title=None, **kwargs):
        """
        :param tr: translation function
        :type tr: callable
        :param parentw: parent window
        :type parentw: Gtk.Window
        :param title: the title of the progressbar window
        :type title: str
        :param operation_cls: the class of the operation
        :type operation_cls: cotinga.core.Operation
        :run_args: all args to provide to the operation.run() method
        :type run_args: tuple
        """
        self.tr = tr
        self.parentw = parentw
        self.finished_msg = finished_msg
        self.aborted_msg = aborted_msg
        if finished_title is None:
            finished_title = self.tr('Finished!')
        self.finished_title = finished_title
        if aborted_title is None:
            aborted_title = self.tr('Aborted.')
        self.aborted_title = aborted_title

        self.finished_state = ['emblem-default', Gtk.IconSize.LARGE_TOOLBAR]
        self.aborted_state = ['emblem-unreadable', Gtk.IconSize.LARGE_TOOLBAR]

        self.operation = operation_cls(self.tr)
        self.operation.connect('operation-finished',
                               self.on_operation_finished)
        self.operation.connect('operation-aborted', self.on_operation_aborted)
        self.run_args = run_args

        super().__init__(*args, **kwargs)

        self.state_icon = Gtk.Image()

        self.content = Gtk.Grid()
        self.info_label = Gtk.Label(title)
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
        self.add(self.content)
        self.set_icon_from_file(COTINGA_ICON)
        self.set_title(title)
        self.set_keep_above(True)

    def run_operation(self):
        thread = threading.Thread(target=self.operation.run,
                                  args=self.run_args)
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

    def on_operation_finished(self, *args):
        self._handle_signal_from_external_thread(self.finished_title,
                                                 self.finished_msg,
                                                 self.finished_state)

    def on_operation_aborted(self, *args):
        self._handle_signal_from_external_thread(self.aborted_title,
                                                 self.aborted_msg,
                                                 self.aborted_state)

    def on_ok_clicked(self, *args):
        self.close()
