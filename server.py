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
    questions = data_manager.select_sql(
        'question', order_column='submission_time', order_asc_desc='DESC'
    )
    return render_template('list_all.html', questions=questions)


@app.route('/question/<int:question_id>')
def show_question(question_id):
    question = data_manager.select_sql('question', clause='WHERE', condition=['id', '=', question_id])
    answers = data_manager.select_sql('question', clause='WHERE', condition=['id', '=', question_id])
    if not answers:
        answers = [{'Answers': 'This question doesn\'t has any answer yet.'}]
    question[0]['view_number'] += 1
    data_manager.update_sql(
        table='question', column='view_number',
        update_value=question[0]['view_number'], update_condition=f'id={question_id}'
    )
    return render_template('display_question.html', question=question, answers=answers, question_id=question_id)


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


@app.route('/debug-url')
def asdasd():
    print(strftime("%Y-%m-%d %H:%M:%S.%F", gmtime()))
    return redirect('/')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
