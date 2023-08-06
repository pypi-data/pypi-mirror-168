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

import json
from pathlib import Path

from microlib import XDict


def load(filename):
    """Load the values from the jsonl file."""
    return json.loads(Path(filename).read_text())


def save(data, filename):
    """Save the given file, but updated with given data."""
    content = XDict(json.loads(Path(filename).read_text()))
    content.recursive_update(data)
    Path(filename).write_text(json.dumps(content))
