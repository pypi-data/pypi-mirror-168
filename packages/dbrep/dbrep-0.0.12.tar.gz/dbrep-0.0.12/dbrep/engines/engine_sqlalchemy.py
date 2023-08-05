
# Performance notes (based on simple test, without detailed hyperparameters and size comparisons):
# 1) pandas uses sqlalchemy with execute(table.insert(), data) -- set it as baseline
#    there are 3 option for insert method: None, 'multi' and custom (e.g. PG COPY)
# 2) None is versatile and fastest (100% time)
# 3) 'multi' is unexpectedly slower (700% time)
# 4) PG COPY is much faster (30% time)
# 5) None performance is attained using sqlalchemy.execute and passing list of dictionaries for bind params
# 6) Much faster alternative is insert values (), (), (), () using mogrify on python side ~50% time
#
# HENCE primary solution to test against pandas: mogrify inside python, insert with several simple executes

import functools

from .engine_base import BaseEngine
from . import add_engine_factory

class SQLAlchemyEngine(BaseEngine):
    id = 'sqlalchemy'
    
    @staticmethod
    def _make_query_from_config( config):
        if 'query' in config:
            return '({}) t'.format(config['query'])
        if 'schema' in config:
            return '{}.{}'.format(config['schema'], config['table'])
        return '{}'.format(config['table'])

    def __init__(self, connection_config):
        import sqlalchemy #import only here when it will be actually used
        def make_table_(table_name, schema_name, col_names):
            meta = sqlalchemy.MetaData()
            table_kw = {}
            if schema_name:
                table_kw['schema'] = schema_name
            return sqlalchemy.Table(table_name, meta,
                        *[sqlalchemy.Column(x) for x in col_names],
                        **table_kw
                    )

        self.engine = sqlalchemy.create_engine(connection_config['conn-str'], **connection_config.get('sqlalchemy-config', {}))
        self.conn = self.engine.connect()
        self.template_select_inc = 'select * from {src} where {rid} > {rid_value} order by {rid}'
        self.template_select_inc_null = 'select * from {src} order by {rid}'
        self.template_select_all = 'select * from {src}'
        self.template_select_rid = 'select max({rid}) from {src}'
        self.make_query = sqlalchemy.text
        self.make_table = lambda table_name, schema_name, col_names: make_table_(table_name, schema_name, col_names)
        self.active_insert = None
        self.active_cursor = None

    def _execute(self, *args, **kwargs):
        try:
            return self.conn.execute(*args, **kwargs)
        except ConnectionError:
            self.conn = self.engine.connect()
            return self.conn.execute(*args, **kwargs)


    def get_latest_rid(self, config):
        query = self.make_query(self.template_select_rid.format(
            src=SQLAlchemyEngine._make_query_from_config(config),
            rid=config['rid']
        ))
        res = self._execute(query).fetchall()
        if res is None or len(res) == 0:
            return None
        return res[0][0]

    def begin_incremental_fetch(self, config, min_rid):
        template = self.template_select_inc if min_rid else self.template_select_inc_null
        query = self.make_query(template.format(
            src=SQLAlchemyEngine._make_query_from_config(config),
            rid=config['rid'],
            rid_value=min_rid
        ))
        self.active_cursor = self._execute(query)

    def begin_full_fetch(self, config):
        query = self.make_query(self.template_select_all.format(
            src=SQLAlchemyEngine._make_query_from_config(config)
        ))
        self.active_cursor = self._execute(query)

    def begin_insert(self, config):
        self.active_insert = functools.partial(self.make_table, table_name=config['table'], schema_name=config.get('schema'))

    def fetch_batch(self, batch_size):
        if not self.active_cursor:
            raise Exception("No active cursor!")
        keys = list(self.active_cursor.keys())
        return keys, self.active_cursor.fetchmany(batch_size)

    def insert_batch(self, names, batch):
        self._execute(self.active_insert(col_names=names).insert(), [dict(zip(names, x)) for x in batch])

    def close(self):
        self.conn.close()
        self.engine.dispose()

add_engine_factory(SQLAlchemyEngine)