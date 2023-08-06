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
    from gi.repository import GObject


class Operation(GObject.Object):

    @GObject.Signal
    def operation_finished(self):
        """Notify that the operation is finished."""

    @GObject.Signal
    def operation_aborted(self):
        """Notify that the operation has been aborted."""

    def __init__(self, tr, *kwargs):
        GObject.Object.__init__(self, *kwargs)
        self.tr = tr

    def run(self, *run_args):
        raise NotImplementedError('The run() method must be redefined')


class MathmakerGenerateOperation(Operation):

    def run(self, *run_args):
        pass
