import csv
import hashlib
import os
import re
from abc import abstractmethod
from typing import Callable

import nure.sync.cache
import sqlalchemy


class Sql(nure.sync.cache.LocalFileCache):
    def __init__(self, suffix_func: Callable, root_path='data/sql', ttl=None) -> None:
        super(Sql, self).__init__(root_path, ttl)
        self.suffix_func = suffix_func

    @property
    @abstractmethod
    def engine(self) -> sqlalchemy.engine.Engine:
        raise NotImplementedError()

    def key_to_local_relative_path(self, key: str, *args, **kargs) -> str:
        if os.path.isfile(key):
            fn, _ = os.path.splitext(os.path.basename(key))
        else:
            fn = hashlib.md5(key.encode('utf8')).hexdigest()
        suffix = self.suffix_func(*args, **kargs)
        return f'{fn}{suffix}.csv'

    def retrieve(self, sql_key: str, local_file_path: str,
                 re_replace=None, sa_replace=None, partition_size=10000):
        if os.path.isfile(sql_key):
            with open(sql_key, 'rt') as fd:
                sql_str = fd.read()
        else:
            sql_str = sql_key

        if isinstance(re_replace, dict):
            for pattern, repl in re_replace.items():
                sql_str = re.sub(pattern, repl, sql_str)

        with self.engine.connect().execution_options(stream_results=True) as conn:
            conn: sqlalchemy.engine.Connection
            result: sqlalchemy.engine.ResultProxy = conn.execute(sqlalchemy.text(sql_str), sa_replace or {})

            with open(local_file_path, 'wt', newline='') as csv_file:
                writer = csv.writer(csv_file, dialect='excel')
                writer.writerow(result.keys())

                while len(rows := result.fetchmany(size=partition_size)) > 0:
                    writer.writerows(rows)
