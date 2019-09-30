import database_common


@database_common.connection_handler
def get_latest_5_answers(cursor):
    cursor.execute("""SELECT * FROM question ORDER BY submission_time DESC LIMIT 5;""")
    latest_5_answers = cursor.fetchall()
    return latest_5_answers

