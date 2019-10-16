from flask import Flask, render_template, request, redirect, escape, session, url_for
from time import gmtime, strftime

import data_manager

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def index():
    latest_5_questions = data_manager.select_sql(
        'question', order_column='submission_time', order_asc_desc='DESC', limit='5'
    )
    login_status_message = 'You are not logged in'
    if 'user_name' in session:
        login_status_message = 'Logged in as %s' % escape(session['user_name'])
        
    return render_template('index.html', questions=latest_5_questions, login_status_message=login_status_message)


@app.route('/list')
def list_all():
    if request.args:
        questions = data_manager.select_sql(
            'question', order_column=[*request.args.keys()][0], order_asc_desc=[*request.args.values()][0]
        )
        return render_template('list_all.html', questions=questions)
    questions = data_manager.select_sql(
        'question', order_column='submission_time', order_asc_desc='DESC'
    )
    return render_template('list_all.html', questions=questions)


@app.route('/picture/<path:picture>')
def show_picture(picture):
    return render_template('picture.html', picture=picture, return_url=request.referrer)


@app.route('/question/<int:question_id>')
def show_question(question_id):
    question = data_manager.select_sql('question', clause='WHERE', condition=['id', '=', question_id])
    answers = data_manager.select_sql('answer', clause='WHERE', condition=['question_id', '=', question_id])
    comments = data_manager.select_sql('comment', clause='WHERE', condition=['question_id', '=', question_id])
    comment_head = data_manager.get_table_head('comment')
    if not answers:
        answers = [{'Answers': 'This question doesn\'t have any answer yet.'}]
    if not comments:
        comment_head = ['Comments']
        comments = [{'Comments': 'This answer doesn\'t have any comment yet.'}]
    question[0]['view_number'] += 1
    data_manager.update_sql(
        table='question', column='view_number',
        update_value=question[0]['view_number'], update_condition=f'id={question_id}'
    )
    return render_template(
        'display_question.html', question=question, answers=answers, comments=comments, question_id=question_id,
        comment_head=comment_head
    )


@app.route('/<table>/<int:id_>/vote-<vote_direction>')
def vote(id_, vote_direction, table):
    table_data = data_manager.select_sql(table, clause='WHERE', condition=['id', '=', id_])
    if vote_direction == 'up':
        table_data[0]['vote_number'] += 1
    elif vote_direction == 'down':
        table_data[0]['vote_number'] -= 1
    data_manager.update_sql(
        table=table, column='vote_number',
        update_value=table_data[0]['vote_number'], update_condition=f'id={id_}'
    )
    if table == 'answer':
        id_ = table_data[0]['question_id']
    question = data_manager.select_sql('question', clause='WHERE', condition=['id', '=', id_])
    question[0]['view_number'] -= 1
    data_manager.update_sql(
        table='question', column='view_number',
        update_value=question[0]['view_number'], update_condition=f'id={id_}'
    )
    return redirect(f'/question/{id_}')


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    table_head = data_manager.get_table_head('question')
    if request.method == 'POST':
        user_id = data_manager.select_sql(
            'users', clause='WHERE', condition=['user_name', '=', session['user_name']]
        )
        new_record = {table_head[1]: str(strftime("%Y-%m-%d %H:%M:%S", gmtime())),
                      table_head[2]: '0',
                      table_head[3]: '0',
                      table_head[4]: request.form[table_head[4]],
                      table_head[5]: request.form[table_head[5]],
                      table_head[6]: f'{request.form[table_head[6]] if request.form[table_head[6]] else None}',
                      table_head[7]: str(user_id[0]['id'])}
        data_manager.insert_record('question', new_record)
        new_record_id = data_manager.select_sql(
            'question', column='id', clause='WHERE', condition=[table_head[1], '=', new_record[table_head[1]]]
        )
        return redirect(f'/question/{new_record_id[0]["id"]}')
    return render_template('new_question.html', table_head=table_head)


@app.route('/question/<int:question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    table_head = data_manager.get_table_head('question')
    question = data_manager.select_sql('question', clause='WHERE', condition=['id', '=', question_id])
    if request.method == 'POST':
        for column_name, element in request.form.items():
            data_manager.update_sql('question', column_name, element, update_condition=f'id={question_id}')
        return redirect(f'/question/{question_id}')
    return render_template('update_question.html', table_head=table_head, question=question, question_id=question_id)


@app.route('/question/<int:question_id>/delete', methods=['GET', 'POST'])
def delete_question(question_id):
    data_manager.delete_record('comment', clause='WHERE', condition=['question_id', '=', question_id])
    data_manager.delete_record('answer', clause='WHERE', condition=['question_id', '=', question_id])
    data_manager.delete_record('question', clause='WHERE', condition=['id', '=', question_id])
    return redirect('/')


@app.route('/question/<int:question_id>/new-answer', methods=['GET', 'POST'])
def add_answer(question_id):
    table_head = data_manager.get_table_head('answer')
    if request.method == 'POST':
        user_id = data_manager.select_sql(
            'users', clause='WHERE', condition=['user_name', '=', session['user_name']]
        )
        new_record = {table_head[1]: str(strftime("%Y-%m-%d %H:%M:%S", gmtime())),
                      table_head[2]: '0',
                      table_head[3]: str(question_id),
                      table_head[4]: request.form[table_head[4]],
                      table_head[5]: f'{request.form[table_head[5]] if request.form[table_head[5]] else None}',
                      table_head[6]: str(user_id[0]['id'])}
        data_manager.insert_record('answer', new_record)
        return redirect(f'/question/{question_id}')
    return render_template('new_answer.html', table_head=table_head, question_id=question_id)


@app.route('/answer/<int:answer_id>/delete')
def delete_answer(answer_id):
    data_manager.delete_record('comment', clause='WHERE', condition=['answer_id', '=', answer_id])
    data_manager.delete_record('answer', clause='WHERE', condition=['id', '=', answer_id])
    return redirect('/')


@app.route('/search')
def search():
    questions = data_manager.select_sql(
        'question', clause='WHERE', condition=['title', 'LIKE', '%' + [*request.args.values()][0] + '%'],
        clause_operator='OR', condition2=['message', 'LIKE', '%' + [*request.args.values()][0] + '%']
    )
    answer_id = data_manager.select_sql(
        'answer', clause='WHERE', condition=['message', 'LIKE', '%' + [*request.args.values()][0] + '%'])
    answer_id = [*{i['question_id'] for i in answer_id}]
    for item in answer_id:
        if item not in [*{i['id'] for i in questions}]:
            questions += data_manager.select_sql('question', clause='WHERE', condition=['id', '=', item])
    if questions:
        return render_template('fancy_search.html', questions=questions, search_frase=[*request.args.values()][0])
    return redirect('/')


@app.route('/answer/<int:answer_id>')
def show_answer(answer_id):
    answer = data_manager.select_sql('answer', clause='WHERE', condition=['id', '=', answer_id])
    comments = data_manager.select_sql('comment', clause='WHERE', condition=['answer_id', '=', answer_id])
    comment_head = data_manager.get_table_head('comment')
    if not comments:
        comments = [{'Comments': 'This answer doesn\'t have any comments yet.'}]
    return render_template(
        'display_answer.html', answer=answer, comments=comments, comment_head=comment_head,
        answer_id=answer_id, question_id=answer[0]['question_id']
    )


@app.route('/answer/<int:answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    table_head = data_manager.get_table_head('answer')
    answer = data_manager.select_sql('answer', clause='WHERE', condition=['id', '=', answer_id])
    if request.method == 'POST':
        for column_name, element in request.form.items():
            data_manager.update_sql('answer', column_name, element, update_condition=f'id={answer_id}')
        return redirect(f'/answer/{answer_id}')
    return render_template('update_answer.html', table_head=table_head, answer=answer, answer_id=answer_id)


@app.route('/<table_name>/<id_>/new-comment', methods=['GET', 'POST'])
def add_comment(table_name, id_):
    comment_head = data_manager.get_table_head('comment')
    if request.method == 'POST':
        if table_name == 'question':
            new_record = {comment_head[1]: id_,
                          comment_head[3]: request.form[comment_head[3]],
                          comment_head[4]: str(strftime("%Y-%m-%d %H:%M:%S", gmtime())),
                          comment_head[5]: '0'
                          }
            data_manager.insert_record('comment', new_record)
        elif table_name == 'answer':

            new_record = {comment_head[1]: '0', comment_head[2]: id_,
                          comment_head[3]: request.form[comment_head[3]],
                          comment_head[4]: str(strftime("%Y-%m-%d %H:%M:%S", gmtime())),
                          comment_head[5]: '0'
                          }
            data_manager.insert_record('comment', new_record)
        return redirect(f'/{table_name}/{id_}')
    return render_template('new_comment.html', table_head=comment_head, table_name=table_name, id=id_)


@app.route('/comments/<int:comment_id>/edit', methods=['GET', 'POST'])
def edit_comment(comment_id):
    table_head = data_manager.get_table_head('comment')
    comment = data_manager.select_sql(
        table='comment', clause='WHERE', condition=['id', '=', comment_id]
    )
    if comment[0]['answer_id'] is None:
        redirect_table = 'question'
        redirect_id = comment[0]['question_id']
    else:
        redirect_table = 'answer'
        redirect_id = comment[0]['answer_id']
    if request.method == 'POST':
        for column_name, element in request.form.items():
            data_manager.update_sql('comment', column_name, element, update_condition=f'id={comment_id}')
        data_manager.update_sql(
            'comment', 'edited_count', comment[0]['edited_count'] + 1, update_condition=f'id={comment_id}'
        )
        return redirect(f'/{redirect_table}/{redirect_id}')
    return render_template(
        'update_comment.html', table_head=table_head, comment=comment,
        redirect_id=redirect_id, redirect_table=redirect_table
    )


@app.route('/comments/<id_>/delete')
def delete_comment(id_):
    comment_row = data_manager.select_sql(
        table='comment', clause='WHERE', condition=['id', '=', id_]
    )
    if comment_row[0]['answer_id'] is None:
        redirect_table = 'question'
        redirect_id = comment_row[0]['question_id']
    else:
        redirect_table = 'answer'
        redirect_id = comment_row[0]['answer_id']
    data_manager.delete_record(table='comment', clause='WHERE', condition=['id', '=', id_])
    return redirect(f'/{redirect_table}/{redirect_id}')


@app.route('/registration', methods=['GET', 'POST'])
def user_registration():
    user_name_exists = False
    if request.method == 'POST':
        if request.form['user_name'] not in \
                [row['user_name'] for row in data_manager.select_sql(table='users', column='user_name')]:
            hashed_password = data_manager.hash_password(request.form['password'])
            data_manager.insert_record('users', {'user_name': request.form['user_name'], 'password': hashed_password})
            return redirect('/registration')
        user_name_exists = True
    return render_template('new_user.html', user_name_exists=user_name_exists)


@app.route('/login', methods=['GET', 'POST'])
def user_login():
    login_fail = False
    if request.method == 'POST' and request.form:
        if request.form['user_name'] in [row['user_name'] for row in data_manager.select_sql(
                table='users', column='user_name')]:
            if data_manager.verify_password(request.form['password'], data_manager.select_sql(
                    column='password', table='users', clause='WHERE',
                    condition=['user_name', '=', request.form['user_name']])[0]['password']):
                session['user_name'] = request.form['user_name']
                return redirect('/')
        login_fail = True
    return render_template('login_user.html', login_fail=login_fail)


@app.route('/logout', methods=['GET', 'POST'])
def user_logout():
    session.pop('user_name', None)
    return redirect(url_for('index'))


@app.route('/debug-url')
def asdasd():
    return redirect('/')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
