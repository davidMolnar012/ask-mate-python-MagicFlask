import psycopg2
import database_common


@database_common.connection_handler
def show_all(cursor):
    cursor.execute("""SELECT * FROM mentors ORDER BY id;""")
    mentor_names = cursor.fetchall()
    cursor.execute("""SELECT * FROM applicants ORDER BY id;""")
    applicant_names = cursor.fetchall()
    return mentor_names, applicant_names


@database_common.connection_handler
def get_mentor_names_by_first_name(cursor, first_name):
    cursor.execute("""
                    SELECT first_name, last_name FROM mentors
                    WHERE first_name = %(first_name)s ORDER BY first_name;
                   """,
                   {'first_name': first_name})
    names = cursor.fetchall()
    return names


@database_common.connection_handler
def get_full_names(cursor):
    cursor.execute("""
                    SELECT first_name, last_name FROM mentors;
                   """)
    names = cursor.fetchall()
    return names


@database_common.connection_handler
def get_nick_names(cursor, city_name):
    cursor.execute("""
                    SELECT nick_name FROM mentors
                    WHERE city=%(city_name)s;
                   """, {'city_name': city_name})
    names = cursor.fetchall()
    return names


@database_common.connection_handler
def get_last_name(cursor, first_name):
    cursor.execute("""
                    SELECT first_name, last_name, phone_number FROM applicants
                    WHERE first_name = %(first_name)s;
                   """,
                   {'first_name': first_name})
    names = cursor.fetchall()
    return names


@database_common.connection_handler
def get_last_name(cursor, first_name):
    cursor.execute("""
                    SELECT first_name, last_name, phone_number FROM applicants
                    WHERE first_name = %(first_name)s;
                   """,
                   {'first_name': first_name})
    names = cursor.fetchall()
    return names


@database_common.connection_handler
def get_name_by_email_address(cursor, email_address):
    email_address = "%" + email_address + "%"
    cursor.execute("""
                    SELECT first_name, last_name, phone_number, email FROM applicants
                    WHERE email LIKE %(email_address)s;
                   """,
                   {'email_address': email_address})
    names = cursor.fetchall()
    return names


@database_common.connection_handler
def add_applicant(cursor, applicant_dict):
    try:
        cursor.execute(
            """INSERT INTO applicants (first_name,last_name,phone_number,email,application_code)
            VALUES (%(first_name)s, %(last_name)s, %(phone_number)s, %(email_address)s,%(application_code)s);""",
            {
                'first_name': applicant_dict['first_name'],
                'last_name': applicant_dict['last_name'],
                'phone_number': applicant_dict['phone_number'],
                'email_address': applicant_dict['email_address'],
                'application_code': applicant_dict['application_code']
            })
        cursor.execute(
            """SELECT * FROM applicants
               WHERE application_code = %(application_code)s;""",
            {
                'application_code': applicant_dict['application_code']
            }
        )
    except psycopg2.DatabaseError as exception:
        return [{'1': exception}]
    names = cursor.fetchall()
    return names


@database_common.connection_handler
def remove_applicant(cursor, application_code):
    cursor.execute("""DELETE FROM applicants
                      WHERE application_code = %(application_code)s;""",
                   {'application_code': application_code})@database_common.connection_handler


@database_common.connection_handler
def update_applicant_phone_number_by_name(cursor, first_name, last_name , phone_number):
    cursor.execute("""UPDATE applicants SET phone_number = %(phone_number)s
                      WHERE first_name = %(first_name)s AND last_name = %(last_name)s;""",
                   {'first_name': first_name,
                    'last_name': last_name,
                    'phone_number': phone_number})
    cursor.execute("""SELECT * FROM applicants
                    WHERE first_name = %(first_name)s AND last_name = %(last_name)s;""",
                   {'first_name': first_name,
                    'last_name': last_name,
                    'phone_number': phone_number})
    name = cursor.fetchall()
    return name


@database_common.connection_handler
def remove_applicant_by_email(cursor, email_address):
    email_address = '%' + email_address + '%'
    cursor.execute("""DELETE FROM applicants
                      WHERE email LIKE %(email_address)s;""",
                   {'email_address': email_address})
