# db_functions.py
# -*- coding: utf-8 -*-

"""
Functions which serve for database purposes
"""

import sqlalchemy as sa
from collections import namedtuple

from .util_functions import input_prompt


# ______________________________________________________________________________________________________________________


def create_db_engine(db_cfg: dict, db_conn_info: dict, db_name: str = None) -> tuple:
    """
    Opens a connection to a database you can choose or specify upfront

    Args:
        db_cfg: dictionary containing the configuration information for the database
        db_conn_info: dictionary with the available database names as keys and connection information as values
        db_name: (optional) name of database, if None lets you choose from all available databases

    Returns:
        a named tuple with the following fields: db_name, engine
    """

    # db_cfg = cfg.Database.toDict(); db_conn_info = db_available; db_name = None; verbose = True

    fields = ('db_name', 'engine')
    DB = namedtuple('DB', fields, defaults=(None,) * len(fields))

    if not db_name:
        db_name = input_prompt(
            name='database',
            choices=tuple(db_conn_info.keys()),
            enum=True,
        )

    conn_str = None
    if db_cfg[db_name]['type'] == 'MS SQL Server':
        conn_str = db_cfg[db_name]['driver'] + ':///?odbc_connect='
    elif db_cfg[db_name]['type'] in ('MariaDB', 'PostgreSQL'):
        conn_str = db_cfg[db_name]['driver'] + '://'
    elif db_cfg[db_name]['type'] == 'SQLite3':
        conn_str = db_cfg[db_name]['driver'] + ':///'
    conn_str += str(db_conn_info[db_name])

    engine = sa.create_engine(conn_str)

    return DB(db_name=db_name, engine=engine)


# ______________________________________________________________________________________________________________________


def execute_raw_sql(qry: str, con: sa.engine.Connection | sa.engine.Engine) -> None:
    """
    Executes a sql statement and does not return anything

    Args:
        qry: the sql query to be executed
        con: either the sqlalchemy connection or engine to the database

    Returns:
        Executes and commits the statement against the database and returns None
    """

    con_type = type(con).__name__
    if con_type == 'Engine':
        con = con.connect()
    try:
        con.execute(qry)
    except Exception as ex:
        raise ex
    finally:
        if con_type == 'Engine':
            con.close()

    return None


# ______________________________________________________________________________________________________________________
