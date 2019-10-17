import database_common
from psycopg2 import sql
import bcrypt


@database_common.connection_handler
def select_query(cursor, table, column='', join_type='', join_table='', join_on=[], clause='', condition=[],
                 clause_operator='', condition2=[], group_element='', order_column='', order_asc_desc='', limit='',
                 offset=''):
    """"""
    join_types = ["FULL JOIN", "INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "JOIN"]

    if len(condition) == 3:
        if condition[1].upper() == 'LIKE':
            condition[2] = sql.Literal('%' + condition[2] + '%').as_string(cursor)
        else:
            condition[2] = sql.Literal(condition[2]).as_string(cursor)
    if len(condition2) == 3:
        if condition2[1].upper() == 'LIKE':
            condition2[2] = sql.Literal('%' + condition2[2] + '%').as_string(cursor)
        else:
            condition2[2] = sql.Literal(condition2[2]).as_string(cursor)
    if column == '*':
        column = sql.Identifier(column)

    query = sql.SQL(
        f'SELECT {"{}" if column else "*"} FROM {{}} '
        f'{join_type + " " + join_table + " " if join_type in join_types else ""}'
        f'{"ON " + join_on[0] + "=" + join_on[1] + " " if len(join_on) == 2 else ""}'
        f'{clause + " " if clause.upper() in ["WHERE"] else ""}'
        f'{condition[0] + " " + condition[1] + " " + condition[2] + " " if len(condition) == 3 else ""}'
        f'{clause_operator + " " if clause_operator.upper() in ["AND", "OR"] else ""}'
        f'{condition2[0] + " " + condition2[1] + " " + condition2[2] + " " if len(condition2) == 3 else ""}'
        f'{"GROUP BY " + group_element + " " if group_element else ""}'
        f'{"ORDER BY " + order_column + " " if order_column else ""}'
        f'{order_asc_desc + " " if order_asc_desc == "ASC" or "DESC" else ""}'
        f'{"LIMIT " + limit + " " if limit.isdigit() else ""}'
        f'{"OFFSET " + offset if offset.isdigit() else ""}'
        ';'
    )
    if column:
        query = query.format(sql.Identifier(column), sql.Identifier(table))
    else:
        query = query.format(sql.Identifier(table))
    cursor.execute(query)
    print(cursor.query)
    return cursor.fetchall()


@database_common.connection_handler
def update_query(cursor, table, column, update_value, update_condition=''):
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
    cursor.execute(sql.SQL(
        f'DELETE FROM {table} {clause} {condition[0] + condition[1] + condition[2] if len(condition) == 3 else ""}')
    )


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


def get_user_names():
    users = select_query(table='users', order_column='id', order_asc_desc='ASC')
    user_name = {}
    for item in users:
        user_name[item['id']] = item['user_name']
    return user_name
