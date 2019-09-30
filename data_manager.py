import database_common


@database_common.connection_handler
def show_all(cursor):
    cursor.execute("""SELECT * FROM mentors ORDER BY id;""")
    mentor_names = cursor.fetchall()
    cursor.execute("""SELECT * FROM applicants ORDER BY id;""")
    applicant_names = cursor.fetchall()
    return mentor_names, applicant_names

