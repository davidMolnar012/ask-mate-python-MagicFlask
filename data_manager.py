import database_common


@database_common.connection_handler
def get_latest_answers(cursor, limit=''):
    if limit == '':
        cursor.execute("""SELECT * FROM question ORDER BY submission_time DESC;""")
    else:
        cursor.execute("""SELECT * FROM question ORDER BY submission_time DESC
         LIMIT %(limit)s  ;""", {'limit': limit})
    return cursor.fetchall()


