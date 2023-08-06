"""
Functions and helper functions to sync tables in a database
"""
import logging
import psycopg
from typing import List


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def get_n_records_in_table(cur: psycopg.Cursor, table_name: str) -> int:
    """
    Get the number of records in a table
    """
    sql_count = f"""SELECT COUNT(*) FROM {table_name}"""
    cur.execute(sql_count)
    n_records = cur.fetchone()[0]
    return n_records


def copy_records(cur_source: psycopg.Cursor, con_destination: psycopg.Connection, table_name,
                 offset: int, limit: int) -> int:
    """
    Copy records from a table using offset and limit.

    Returns the number of records copied.
    """
    cur_destination = con_destination.cursor()
    logger.debug(f"Fetching {limit} last records from source table {table_name} using offset "
                 f"{offset}")
    sql_select = f"""SELECT * FROM {table_name} OFFSET {offset} LIMIT {limit}"""
    cur_source.execute(sql_select)
    records = cur_source.fetchall()
    n_records = len(records)
    logger.debug(f"Fetched {n_records} records in source table {table_name}")
    if n_records > 0:
        logger.debug(f"Inserting {n_records} records in destination table {table_name}")
        n_fields = len(records[0])
        sql_insert = f"""INSERT INTO {table_name} VALUES ({','.join(['%s'] * n_fields)})"""
        cur_destination.executemany(sql_insert, records)
        con_destination.commit()
        logger.debug(f"Inserted {n_records} records in destination table {table_name}")
    else:
        logger.debug(f"Nothing to insert in destination table {table_name}")
    return n_records


def sync_table(cur_source: psycopg.Cursor, con_destination: psycopg.Connection, table_name: str,
               chunk_size: int) -> None:
    """
    Sync a single table.

    Divide sync volume into chunks of count chunk_size.
    """
    logger.info(f"Syncing table {table_name}")
    n_records_source = get_n_records_in_table(cur_source, table_name)
    n_records_destination = get_n_records_in_table(con_destination.cursor(), table_name)
    logger.info(f"Table {table_name} has source records: {n_records_source}, "
                f"destination records: {n_records_destination}")
    if n_records_source > n_records_destination:
        logger.info(f"Start syncing {n_records_source- n_records_destination} records of "
                    f"table {table_name} in chunks of size {chunk_size}")
        for offset in range(n_records_destination, n_records_source, chunk_size):
            copy_records(cur_source=cur_source, con_destination=con_destination,
                         table_name=table_name, offset=offset, limit=chunk_size)
        logger.info(f"Syncing of table {table_name} completed.")
    else:
        logger.info(f"Destination table {table_name} is up to date. Nothing to do.")


def sync(cur_source: psycopg.Cursor, con_destination: psycopg.Connection, tables: List[str],
         chunk_size: int = 1) -> None:
    """
    Sync tables in a database.

    Divide sync volume into chunks of count chunk_size.
    """
    logger.info(f"Syncing tables {tables}")
    for table in tables:
        sync_table(cur_source, con_destination, table, chunk_size)
    logger.info(f"Syncing of tables {tables} completed.")
