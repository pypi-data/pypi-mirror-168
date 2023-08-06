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

from cotinga.gui.core.list_manager import ListManagerPanel


class ClassesManagerPanel(ListManagerPanel):

    def __init__(self, db, status, prefs, recollections,
                 data_list, data_title, mini_items_nb=2, presets=None,
                 locked=None, store_types=None, reorderable=True,
                 editable=None, setup_buttons_icons=True, enable_buttons=True,
                 parentw=None, classes_renamed=None):
        ListManagerPanel.__init__(self, db, status, prefs, recollections,
                                  data_list, data_title,
                                  mini_items_nb=mini_items_nb, presets=presets,
                                  locked=locked, store_types=store_types,
                                  reorderable=reorderable, editable=editable,
                                  setup_buttons_icons=setup_buttons_icons,
                                  enable_buttons=enable_buttons,
                                  parentw=parentw)
        # To track renamed classes
        if classes_renamed is None:
            classes_renamed = []
        self.classes_renamed = classes_renamed

    def on_cell_edited(self, widget, path, new_text, col_nb=0,
                       forbid_empty_cell=True,
                       forbid_duplicate_content=True,
                       forbid_internal_sep=True,
                       change_is_required=True,
                       do_cleanup=True,
                       cell_store_type=None,
                       cell_store_kwargs=None):
        id_value, model, treeiter, _ = self.get_selection_info()
        old_text = model.get(treeiter, col_nb)[0]
        accepted, _ = ListManagerPanel\
            .on_cell_edited(self, widget, path, new_text,
                            col_nb=col_nb, forbid_empty_cell=forbid_empty_cell,
                            forbid_duplicate_content=forbid_duplicate_content,
                            forbid_internal_sep=forbid_internal_sep,
                            change_is_required=change_is_required,
                            do_cleanup=do_cleanup,
                            cell_store_type=cell_store_type,
                            cell_store_kwargs=cell_store_kwargs)
        if accepted:  # new entry is accepted (no duplicate etc.)
            self.classes_renamed.append((old_text, new_text))
            print(f'renamed: {self.classes_renamed}')
