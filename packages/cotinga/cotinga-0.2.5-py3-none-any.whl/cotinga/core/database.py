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

from gettext import translation

from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker, mapper, clear_mappers
from sqlalchemy import create_engine, MetaData, Table

from microlib import turn_to_capwords

from cotinga.core import prefs
from cotinga import models
from cotinga.models import TABLENAMES, COLNAMES
from cotinga.core.env import LOCALEDIR, L10N_DOMAIN
from cotinga.core.env import RUNDOC_DB_URI, RUNDOC_DB
from cotinga.core.errors import FileError

__all__ = ['DataBase', 'check_db']


class DataBase(object):

    def __init__(self):
        self.session = None
        self.engine = None
        self.metadata = None

    def new_session(self):
        """Create a new database session."""
        engine = create_engine(RUNDOC_DB_URI, echo=False)
        session = sessionmaker(bind=engine)()
        metadata = MetaData()
        return engine, session, metadata

    def close_session(self):
        """Close the current session."""
        if self.session is not None:
            self.session.close()
        if self.engine is not None:
            self.engine.dispose()
        self.metadata = None
        self.session = None
        self.engine = None
        clear_mappers()

    def terminate_session(self):
        """Close session and remove the file."""
        self.close_session()
        if RUNDOC_DB.is_file():
            RUNDOC_DB.unlink()

    def map_table(self, name):
        """Map a table."""
        model_class = getattr(models, turn_to_capwords(name))
        columns = getattr(models, '{}_columns'.format(name))()
        tablename = getattr(models, '{}_tablename'.format(name))
        table = Table(tablename, self.metadata, *columns)
        mapper(model_class, table)

    def add_table(self, name):
        """Map and create a table in the database if it's not already here."""
        self.map_table(name)
        self.metadata.create_all(self.engine)

    def load_session(self, init=False):
        """
        Create a session for a loaded document or initialize it for a new one.

        :param init: whether the session is for a new document or a loaded one
        :type init: bool
        """
        self.engine, self.session, self.metadata = self.new_session()
        load = self.add_table if init else self.map_table
        for name in TABLENAMES:
            load(name)


def check_db(doc_path):
    """Check database from a file (tables and columns are as expected)."""
    tr = translation(L10N_DOMAIN, LOCALEDIR,
                     [prefs.load()['language']]).gettext
    doc_sqlite_uri = 'sqlite:///{}'.format(doc_path)
    test_engine = create_engine(doc_sqlite_uri, echo=False)
    inspector = inspect(test_engine)
    tested_tablenames = inspector.get_table_names()
    for name in TABLENAMES:
        if name not in tested_tablenames:
            raise FileError(doc_path,
                            msg=tr('Missing table "{tablename}" in the file '
                                   'to load ({filename}).')
                            .format(tablename=name, filename=doc_path))
    for name in tested_tablenames:
        if name not in TABLENAMES:
            raise FileError(doc_path,
                            msg=tr('Found extraneous table "{tablename}" in '
                                   'the file to load ({filename}).')
                            .format(tablename=name, filename=doc_path))
        # LATER: check the columns types too (use col['type']
        # and add a COLTYPES to models/__init__.py)
        tested_colnames = [col['name'] for col in inspector.get_columns(name)]
        for column in COLNAMES[name]:
            if column not in tested_colnames:
                raise FileError(doc_path,
                                msg=tr('Missing column "{column_name}" '
                                       'in table "{tablename}" of the '
                                       'file to load ({filename}).')
                                .format(column_name=column, tablename=name,
                                        filename=doc_path))
        for column in tested_colnames:
            if column not in COLNAMES[name]:
                raise FileError(doc_path,
                                msg=tr('Found extraneous column '
                                       '"{column_name}" '
                                       'in table "{tablename}" of the '
                                       'file to load ({filename}).')
                                .format(column_name=column, tablename=name,
                                        filename=doc_path))
