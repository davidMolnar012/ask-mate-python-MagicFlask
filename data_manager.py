import database_common
from psycopg2 import sql


@database_common.connection_handler
def select_sql(cursor, table, column='*', clause='', condition=[],
               order_column='', order_asc_desc='', limit='', offset=''):
    """"""
    if len(condition) == 3:
        condition[2] = '\'' + str(condition[2]) + '\''
    cursor.execute(sql.SQL(
        f'SELECT {column} FROM {table} '
        f'{clause} {condition[0] + condition[1] + condition[2] if len(condition) == 3 else ""}'
        f'{" ORDER BY " if order_column else ""}{order_column}{" " if order_asc_desc else ""}{order_asc_desc}'
        f'{" LIMIT " if limit else ""}{limit}'
        f'{" OFFSET " if offset else ""}{offset}'
    ))
    return cursor.fetchall()


@database_common.connection_handler
def update_sql(cursor, table, column, update_value, update_condition=''):
    """"""
    cursor.execute(sql.SQL(f'UPDATE {table} SET {column} = \'{update_value}\' '
                           f'{"WHERE " if update_condition else ""}{update_condition}'))


@database_common.connection_handler
def insert_record(cursor, table_name, records):
    """"""
    cursor.execute(sql.SQL(
        f"INSERT INTO {table_name} ({', '.join(records.keys()).rstrip()}) " +
        "VALUES ('{values}')".format(values='\', \''.join(records.values()).rstrip(', \''))))


@database_common.connection_handler
def get_table_head(cursor, table):
    """"""
    cursor.execute(sql.SQL("SELECT column_name FROM information_schema.columns WHERE table_name= '{table}' AND "
                           "table_schema='public'".format(table=table)))
    return [*[i['column_name'] for i in cursor.fetchall()]]


@database_common.connection_handler
def delete_record(cursor, table, clause, condition=[]):
    if len(condition) == 3:
        condition[2] = '\'' + str(condition[2]) + '\''
    cursor.execute(sql.SQL(f'DELETE FROM {table} {clause} {condition[0] + condition[1] + condition[2] if len(condition) == 3 else ""}'))

