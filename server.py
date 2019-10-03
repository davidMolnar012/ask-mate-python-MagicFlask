from flask import Flask, render_template, request, redirect
from time import gmtime, strftime

import data_manager

app = Flask(__name__)


@app.route('/')
def index():
    latest_5_questions = data_manager.select_sql(
        'question', order_column='submission_time', order_asc_desc='DESC', limit='5'
    )
    return render_template('index.html', questions=latest_5_questions)


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
    
    if not answers:
        answers = [{'Answers': 'This question list_doesn\'t has any answer yet.'}]
    question[0]['view_number'] += 1
    data_manager.update_sql(
        table='question', column='view_number',
        update_value=question[0]['view_number'], update_condition=f'id={question_id}'
    )
    return render_template('display_question.html', question=question, answers=answers, question_id=question_id)


@app.route('/<table>/<int:question_id>/vote-<vote_direction>')
def vote(question_id, vote_direction, table):
    
    table_data = data_manager.select_sql(table, clause='WHERE', condition=['id', '=', question_id])
    if vote_direction == 'up':
        table_data[0]['vote_number'] += 1
    elif vote_direction == 'down':
        table_data[0]['vote_number'] -= 1
    data_manager.update_sql(
        table=table, column='vote_number',
        update_value=table_data[0]['vote_number'], update_condition=f'id={question_id}'
    )

    question = data_manager.select_sql('question', clause='WHERE', condition=['id', '=', question_id])
    question[0]['view_number'] -= 1
    data_manager.update_sql(
        table='question', column='view_number',
        update_value=question[0]['view_number'], update_condition=f'id={question_id}'
    )
    
    return redirect(f'/question/{question_id}')


@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    table_head = data_manager.get_table_head('question')
    if request.method == 'POST':
        new_record = {table_head[1]: str(strftime("%Y-%m-%d %H:%M:%S", gmtime())),
                      table_head[2]: '0', table_head[3]: '0',
                      table_head[4]: request.form[table_head[4]],
                      table_head[5]: request.form[table_head[5]],
                      table_head[6]: f'{request.form[table_head[6]] if request.form[table_head[6]] else None}'}
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
    return render_template('update_question.html', table_head=table_head, question=question, question_id=question_id)


@app.route('/question/<int:question_id>/delete', methods=['GET', 'POST'])
def delete_question(question_id):
    data_manager.delete_record('question', clause='WHERE', condition=['id', '=', question_id])
    return redirect('/')


@app.route('/question/<int:question_id>/new-answer', methods=['GET', 'POST'])
def add_answer(question_id):
    table_head = data_manager.get_table_head('answer')
    if request.method == 'POST':
        new_record = {table_head[1]: str(strftime("%Y-%m-%d %H:%M:%S", gmtime())),
                      table_head[2]: '0', table_head[3]: str(question_id),
                      table_head[4]: request.form[table_head[4]],
                      table_head[5]: f'{request.form[table_head[5]] if request.form[table_head[5]] else None}'}
        data_manager.insert_record('answer', new_record)
        print(new_record)
        return redirect(f'/question/{question_id}')
    return render_template('new_answer.html', table_head=table_head, question_id=question_id)


@app.route('/answer/<int:answer_id>/delete', methods=['GET', 'POST'])
def delete_answer(answer_id):
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
        return render_template('list_all.html', questions=questions)
    return redirect('/')


@app.route('/debug-url')
def asdasd():
    return redirect('/')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
