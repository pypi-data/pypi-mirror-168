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
import tarfile
from tarfile import ReadError, CompressionError
from shutil import move, copyfile
from gettext import translation

import magic

from . import prefs, database
from .env import LOCALEDIR, L10N_DOMAIN
from .env import USER_RUN_DIR, EXTRACTED_DB
from .env import EXTRACTED_DOCSETUP
from .env import RUNDOC_DB, RUN_DOCSETUP, RUNDOC_DIR
from .env import DB_FILENAME, DB_MIMETYPE, DOCSETUP_MIMETYPE
from .env import DOCSETUP_FILENAME
from .env import DEFAULT_RECOLLECTIONS
from .env import EXTRACTED_RECOLL, RECOLLECTIONS_FILENAME
from .env import RECOLLECTIONS_MIMETYPE, RUNDOC_RECOLLECTIONS
from .env import DEFAULT_DOCSETUP
from .errors import FileError
from .tools import is_cot_file

TAR_LISTING_OLD = {DB_FILENAME, DOCSETUP_FILENAME}
TAR_LISTING = TAR_LISTING_OLD | {RECOLLECTIONS_FILENAME}


def new(db):
    """Create and load a new empty document."""
    db.terminate_session()
    copyfile(DEFAULT_DOCSETUP[prefs.load()['language']], RUN_DOCSETUP)
    copyfile(DEFAULT_RECOLLECTIONS, RUNDOC_RECOLLECTIONS)
    db.load_session(init=True)  # Also creates a new pupils.db


def close(db):
    """Close the current document."""
    db.terminate_session()  # Also removes RUNDOC_DB
    if RUN_DOCSETUP.is_file():
        RUN_DOCSETUP.unlink()
    if RUNDOC_RECOLLECTIONS.is_file():
        RUNDOC_RECOLLECTIONS.unlink()


def save_as(dest):
    with tarfile.open(dest, 'w:gz') as tar:
        files_to_add = [os.path.join(RUNDOC_DIR, f)
                        for f in os.listdir(RUNDOC_DIR)
                        if f in TAR_LISTING]
        for f in files_to_add:
            tar.add(f, arcname=os.path.basename(f))


def check_file(doc_name):
    tr = translation(L10N_DOMAIN, LOCALEDIR,
                     [prefs.load()['language']]).gettext
    if not is_cot_file(doc_name):
        raise FileError(doc_name, msg=tr('This file is not a readable '
                                         'compressed archive.'))
    try:
        with tarfile.open(doc_name, mode='r:gz') as archive:
            archived = set(archive.getnames())
            # Allow to open cotinga files from previous versions, without
            # recollections.json
            if archived not in [TAR_LISTING, TAR_LISTING_OLD]:
                raise FileError(doc_name,
                                msg=tr('This archive file does not contain '
                                       'the expected parts (found {}).')
                                .format(archive.getnames()))
            archive.extractall(path=USER_RUN_DIR)
            if archived == TAR_LISTING_OLD:
                copyfile(DEFAULT_RECOLLECTIONS, EXTRACTED_RECOLL)
            db_mimetype_found = magic.from_file(str(EXTRACTED_DB), mime=True)
            if db_mimetype_found not in DB_MIMETYPE:
                raise FileError(doc_name,
                                msg=tr('The database is not correct '
                                       '(found MIME type {}).')
                                .format(db_mimetype_found))
            setup_mimetype_found = magic.from_file(str(EXTRACTED_DOCSETUP),
                                                   mime=True)
            if setup_mimetype_found not in DOCSETUP_MIMETYPE:
                raise FileError(doc_name,
                                msg=tr('The setup part is not correct '
                                       '(found MIME type {}).')
                                .format(setup_mimetype_found))
            recoll_mimetype_found = magic.from_file(str(EXTRACTED_RECOLL),
                                                    mime=True)
            if recoll_mimetype_found not in RECOLLECTIONS_MIMETYPE:
                raise FileError(doc_name,
                                msg=tr('The recollections part is not correct '
                                       '(found MIME type {}).')
                                .format(recoll_mimetype_found))
            database.check_db(EXTRACTED_DB)
    except (ReadError, CompressionError):
        raise FileError(doc_name,
                        msg=tr('This file could not be read or uncompressed '
                               'correctly.'))


def open_(db, terminate_session):
    """
    Set the document in open state.

    check_file() did extract files in run dir; move them to doc run dir.
    Also possibly terminate current session; load the new one.
    """
    if terminate_session:
        db.terminate_session()
    move(EXTRACTED_DB, RUNDOC_DB)
    move(EXTRACTED_DOCSETUP, RUN_DOCSETUP)
    move(EXTRACTED_RECOLL, RUNDOC_RECOLLECTIONS)
    db.load_session()
