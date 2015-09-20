####################################################################################################
#
# PyGeoPortail - A IGN GeoPortail Map Viewer
# Copyright (C) 2015 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

import os

import numpy as np

from PyQt5 import QtCore, QtSql

####################################################################################################

from PyGeoPortail.Math.Interval import IntervalInt

####################################################################################################

class MapLevel(object):

    ##############################################

    def __init__(self, provider_id, map_id, version, level):

        self.provider_id = provider_id
        self.map_id = map_id
        self.version = version
        self.level = level

    ##############################################

    def __str__(self):

        return '{}/{}/{}/{}'.format(self.provider_id, self.map_id, self.version, self.level)

####################################################################################################

class Tile(object):

    ##############################################

    def __init__(self, map_level, row, column):

        self.map_level = map_level
        self.row = row
        self.column = column

    ##############################################

    def __repr__(self):

        pattern = '{provider_id}/{map_id}/{level}/{row}/{column}'
        return pattern.format(provider_id=self.map_level.provider_id,
                              map_id=self.map_level.map_id,
                              level=self.map_level.level,
                              row=self.row,
                              column=self.column)

####################################################################################################

class Run(object):

    ##############################################

    def __init__(self, row, column):

        self.row = row
        self.column = column

    ##############################################

    def __iter__(self):

        for column in self.column.iter():
            yield (self.row, column)

####################################################################################################

class Region(object):

    ##############################################

    def __init__(self, name, map_level, runs):

        self.name = name
        self.map_level = map_level
        self.runs = runs

    ##############################################

    def __iter__(self):

        for run in self.runs:
            for row, column in run:
                yield Tile(self.map_level, row, column)

####################################################################################################

class SqlError(Exception):
    pass

####################################################################################################

class OffLineCache(object):

    ##############################################

    def __init__(self, sqlite_path):

        self._sqlite_path = sqlite_path
        
        create = not os.path.exists(sqlite_path)
        # if not create and os.access(sqlite_path, os.W_OK):
        #     raise NameError('Database is read only')
        
        self._database = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self._database.setDatabaseName(sqlite_path)
        if not self._database.open():
            raise NameError(self._database.lastError().text())
        
        if create:
            self._create_tables()

        self._map_level_id_cache = {}
        self._map_level_cache = {}

    ##############################################

    def __del__(self):

        self._database.close()

    ##############################################

    def _query(self):

        return QtSql.QSqlQuery(self._database)

    ##############################################

    def _commit(self):

        return self._database.commit()

    ##############################################

    def _create_tables(self):

        # https://www.sqlite.org/autoinc.html
        # Fixme: how to handle auto-increment overflow ?
        
        metadata_schema = '''CREATE TABLE metadata (
    version INTEGER
)'''
        
        map_level_schema = '''CREATE TABLE map_level (
    map_level_id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider_id INTEGER,
    map_id INTEGER,
    version INTEGER,
    level INTEGER
)'''
        
        # PRIMARY KEY (map_level_id, row, column),
        tile_schema = '''CREATE TABLE tile (
    map_level_id INTEGER,
    row INTEGER,
    column INTEGER,
    offline_count INTEGER,
    data BLOB,
    FOREIGN KEY(map_level_id) REFERENCES map_level(map_level_id)
)'''
        
        online_cache_schema = '''CREATE TABLE online_cache (
    queue INTEGER,
    map_level_id INTEGER,
    row INTEGER,
    column INTEGER
)'''
        
        # Fixme: id overflow !
        region_schema = '''CREATE TABLE region (
    region_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)'''
        
        region_run_schema = '''CREATE TABLE region_run (
    region_id INTEGER,
    map_level_id INTEGER,
    row INTEGER,
    column_inf INTEGER,
    column_sup INTEGER,
    PRIMARY KEY (region_id, map_level_id, row, column_inf, column_sup),
    FOREIGN KEY(region_id) REFERENCES region(region_id)
    FOREIGN KEY(map_level_id) REFERENCES map_level(map_level_id)
)'''
        
        schemas = (metadata_schema,
                   map_level_schema,
                   tile_schema,
                   online_cache_schema,
                   region_schema,
                   region_run_schema,
        )
        
        query = self._query()
        for sql_query in schemas:
            print(sql_query)
            if not query.exec_(sql_query):
                raise NameError(query.lastError().text())
        self._commit()
        self._init_version()
        self._commit()

    ##############################################

    @staticmethod
    def _join(separator, kwargs):

        # QVariant.toString()
        # QStringList::join
        # $fixme: string require ""
        return separator.join(['{}={}'.format(key, value) for key, value in kwargs.items()])

    ##############################################

    @staticmethod
    def _and_join(kwargs):

        return OffLineCache._join(' AND ', kwargs)

    ##############################################

    @staticmethod
    def _comma_join(kwargs):

        return OffLineCache._join(', ', kwargs)

    ##############################################

    @staticmethod
    def _where_clause_from_object(obj, fields, **kwargs):

        d = {key:getattr(obj, key) for key in fields}
        d.update(kwargs)
        return OffLineCache._and_join(d)

    ##############################################

    def _insert(self, table, commit=False, **kwargs):

        query = self._query()
        fields = kwargs.keys()
        sql_query = 'INSERT INTO ' + table + ' (' + ', '.join(fields) + ') VALUES (' + ', '.join(['?']*len(fields)) + ')'
        print(sql_query)
        query.prepare(sql_query)
        for value in kwargs.values():
            query.addBindValue(value)
        if not query.exec_():
            raise NameError(query.lastError().text())
        if commit:
            self._commit()
        return query

    ##############################################

    def _select(self, table, where='', *args):

        query = self._query()
        sql_query = 'SELECT ' + ', '.join(args) + ' FROM ' + table
        if where:
            sql_query += ' WHERE ' + where
        print(sql_query)
        if not query.exec_(sql_query):
            raise NameError(query.lastError().text())
        return query

    ##############################################

    def _select_one(self, table, where='', *args):

        query = self._select(table, where, *args)
        # if not query.size():
        #     return None
        # elif query.size() >= 1:
        #     raise NameError("More than one rows returned")
        record = query.record()
        if query.next():
            d = {key:query.value(record.indexOf(key)) for key in args}
        else:
            return None
        if query.next():
            raise NameError("More than one rows returned")
        else:
            return d

    ##############################################

    def _delete(self, table, where=''):

        query = self._query()
        sql_query = 'DELETE FROM ' + table
        if where:
            sql_query += ' WHERE ' + where
        print(sql_query)
        if not query.exec_(sql_query):
            raise NameError(query.lastError().text())
        return query

    ##############################################

    def _update(self, table, where='', **kwargs):

        query = self._query()
        sql_query = 'UPDATE ' + table + ' SET ' + self._comma_join(kwargs)
        if where:
            sql_query += ' WHERE ' + where
        print(sql_query)
        if not query.exec_(sql_query):
            raise NameError(query.lastError().text())
        return query

    ##############################################

    def _init_version(self):

        self._insert('metadata', version=1)

    ##############################################

    @staticmethod
    def _map_level_where_clause(map_level):

        return OffLineCache._where_clause_from_object(map_level,
                                                      ('provider_id', 'map_id', 'version', 'level'))

    ##############################################

    def _get_map_level_id(self, map_level):

        map_level_hash = str(map_level)
        if map_level_hash in self._map_level_id_cache:
            return self._map_level_id_cache[map_level_hash]
        else:
            where = self._map_level_where_clause(map_level)
            record = self._select_one('map_level', where, 'map_level_id')
            if record is not None:
                return record['map_level_id']
            else:
                query = self._insert('map_level',
                                     provider_id=map_level.provider_id,
                                     map_id=map_level.map_id,
                                     version=map_level.version,
                                     level=map_level.level,
                                     commit=True
                )
                map_level_id = query.lastInsertId()
                self._map_level_id_cache[map_level_hash] = map_level_id
                return map_level_id

    ##############################################

    def load_map_levels(self):

        args = ('map_level_id', 'provider_id', 'map_id', 'version', 'level')
        query = self._select('map_level', '', *args)
        while query.next():
            record = query.record()
            d = {key:query.value(record.indexOf(key)) for key in args}
            map_level_id = d['map_level_id']
            provider_id, map_id, version, level = d['provider_id'], d['map_id'], d['version'], d['level']
            map_level = MapLevel(provider_id, map_id, version, level)
            self._map_level_cache[map_level_id] = map_level

    ##############################################

    def delete_map_level(self, map_level):

        where = self._map_level_where_clause(map_level)
        self._delete('map_level', where)

    ##############################################

    def vacuum_map_level(self):

        pass
        # Fixme: how to vacuum this table set(from map_level - set(from tile)

    ##############################################

    def insert_tile(self, tile, offline=0):

        # Fixme: check if already there
        # Fixme: could use kwargs
        map_level_id = self._get_map_level_id(tile.map_level)
        data = QtCore.QByteArray(np.ones((2, 2)).tostring())
        self._insert('tile',
                     map_level_id=map_level_id,
                     row=tile.row,
                     column=tile.column,
                     offline_count=offline,
                     data=data
        )

    ##############################################

    def _tile_where_clause(self, tile):

        # Fixme: ???
        if hasattr(tile, 'map_level_id'):
            map_level_id = tile.map_level_id
        else:
            map_level_id = self._get_map_level_id(tile.map_level)
        return self._where_clause_from_object(tile,
                                              ('row', 'column'),
                                              map_level_id=map_level_id)

    ##############################################

    def has_tile(self, tile):

        where = self._tile_where_clause(tile)
        # record = self._select_one('tile', where, 'count()')
        record = self._select_one('tile', where, 'offline_count')
        if record is None:
            return 0
        else:
            return record['offline_count']

    ##############################################

    def get_tile(self, tile):

        where = self._tile_where_clause(tile)
        record = self._select_one('tile', where, 'data')

    ##############################################

    def update_tile_offline_count(self, tile, count):

        where = self._tile_where_clause(tile)
        self._update('tile', where, offline_count=count)

    ##############################################

    def delete_tile(self, tile):

        where = self._tile_where_clause(tile)
        record = self._select_one('tile', where, 'offline_count')
        offline_count = record['offline_count']
        if  offline_count == 1:
            self._delete('tile', where)
        else:
            self.update_tile_offline_count(tile, offline_count-1)

    ##############################################

    def insert_region(self, region, tile_provider):

        record = self._select_one('region', 'name="{}"'.format(region.name), 'count()')
        if record['count()']:
            raise NameError("Region {} already exists".format(region.name))
        query = self._insert('region',
                             name=region.name,
        )
        region_id = query.lastInsertId()
        map_level_id = self._get_map_level_id(region.map_level)
        for run in region.runs:
            self._insert('region_run',
                         region_id=region_id,
                         map_level_id=map_level_id,
                         row=run.row,
                         column_inf=run.column.inf,
                         column_sup=run.column.sup,
            )
        for tile in region:
            # Fixme: map_level_id isn't cached
            offline_count = self.has_tile(tile)
            if offline_count:
                self.update_tile_offline_count(tile, offline_count+1)
            else:
                self.insert_tile(tile, offline=1)

    ##############################################

    def get_region(self):

        pass

    ##############################################

    def delete_region(self, region_id):

        args = ('map_level_id', 'row', 'column_inf', 'column_sup')
        query = self._select('region_run', 'region_id={}'.format(region_id), *args)
        while query.next():
            record = query.record()
            d = {key:query.value(record.indexOf(key)) for key in args}
            map_level_id, row, column_inf, column_sup = d['map_level_id'], d['row'], d['column_inf'], d['column_sup']
            # run = Run(row, IntervalInt(column_inf, column_sup))
            for column in range(column_inf, column_sup +1):
                map_level = None # Fixme: ???
                tile = Tile(map_level, row, column)
                tile.map_level_id = map_level_id
                # if self.has_tile(tile) == 1: # called twice !
                self.delete_tile(tile)
        where = 'region_id={}'.format(region_id)
        self._delete('region_run', where)
        
        # where = self._and_join({'region_id':region_id})
        where = 'region_id={}'.format(region_id)
        self._delete('region', where)

####################################################################################################
#
# End
#
####################################################################################################
