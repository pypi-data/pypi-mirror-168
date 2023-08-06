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

from .preview import PreviewDialog
from .preferences import PreferencesDialog
from .message import run_message_dialog
from .combo import ComboDialog
from .file_open import OpenFileDialog
from .file_save_as import SaveAsFileDialog
from .folder_select import FolderSelectDialog
from .save_before import SaveBeforeDialog
from .confirmation import ConfirmationDialog
from .doc_setup import DocSetupDialog
from .report_setup import ReportSetupDialog

__all__ = [PreferencesDialog, run_message_dialog, OpenFileDialog, ComboDialog,
           SaveAsFileDialog, SaveBeforeDialog, ReportSetupDialog,
           PreviewDialog, ConfirmationDialog, FolderSelectDialog,
           DocSetupDialog, ]
