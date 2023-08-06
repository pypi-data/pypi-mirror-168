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

import sys
import json
import subprocess
from pathlib import Path

from cotinga.core.env import BELTS_JSON
from cotinga.core.presets import TEMPLATE_PREFIX


def _prefix(use_venv=False, venv=''):
    if use_venv and venv:
        path = str(Path(venv) / 'bin/activate').replace(' ', r'\ ')
        return f"source {path}; "
    else:
        return ''


def available_years():
    return ['1', '2']


def is_available(use_venv=False, venv=''):
    cmd = f'{_prefix(use_venv=use_venv, venv=venv)}mathmaker --version'
    ret_code = subprocess.run(cmd, shell=True, executable='/bin/bash',
                              capture_output=True).returncode
    if ret_code:
        return False
    return True


def available_levels(year, use_venv=False, venv=''):
    """mathmaker is assumed to be available"""
    cmd1 = f'{_prefix(use_venv=use_venv, venv=venv)}mathmaker list'
    cmd2 = f'grep y{year}b.*exam'
    cmd = f'{cmd1} | {cmd2}'
    result = subprocess.run(cmd, shell=True, executable='/bin/bash',
                            capture_output=True, text=True).stdout
    return [line.strip().split()[-1] for line in result.split('\n') if line]


def belt_filename(belt):
    return belt.lower()


def create_template(mm_level, belt, use_venv=False, venv='', dest_dir=''):
    tpl_name = f'{TEMPLATE_PREFIX()}{belt}'
    of = f'{belt_filename(belt)}.tex'.replace(' ', r'\ ')
    dest_dir = str(dest_dir).replace(' ', r'\ ')
    options = f'--belts {BELTS_JSON} --shift --cotinga-template "{tpl_name}"'
    cmd = f'cd {dest_dir}; {_prefix(use_venv=use_venv, venv=venv)}'\
        f'mathmaker {options} {mm_level} > {of}'
    print(f'cmd={cmd}')
    return subprocess.run(cmd, shell=True, executable='/bin/bash',
                          capture_output=True).returncode


def get_user_config(use_venv=False, venv=''):
    cmd = f'{_prefix(use_venv=use_venv, venv=venv)}mathmaker config'
    stdout = subprocess.run(cmd, shell=True, executable='/bin/bash',
                            capture_output=True, text=True).stdout
    return json.loads(stdout)


def compile_tex_file(belt, directory=''):
    name = belt_filename(belt)
    p = subprocess.Popen(['lualatex', '-interaction', 'nonstopmode', name],
                         cwd=str(directory), stdout=sys.stderr)
    return p.wait()
