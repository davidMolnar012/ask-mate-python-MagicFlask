from flask import Flask, render_template, request, redirect
import time

import data_handler
import util

app = Flask(__name__)


@app.template_filter('ctime')
def time_ctime(s):
    return time.ctime(int(s))


@app.route('/')
def route_list1():
    user_stories = data_handler.get_all_user_story("question.csv")
    table_head = data_handler.get_data_header("question.csv")
    user_stories = util.dict_sort(user_stories)
    return render_template('list.html', user_stories=user_stories, table_head=table_head)


@app.route('/list')
def route_list2():
    return redirect('/')


@app.route('/question', methods=['GET', 'POST'])
def route_list3():
    questions_head = data_handler.get_data_header("question.csv")
    questions = data_handler.get_all_user_story("question.csv")
    if request.method == 'POST':
        max_id = util.get_max_id(questions)
        new_question = {questions_head[0]: max_id, questions_head[1]: str(round(time.time())),
                        questions_head[2]: '0', questions_head[3]: '0'}
        for key, value in request.form.items():
            new_question[key] = value.replace('\n', '<br>').replace('\r', '')
        data_handler.write_new_story(new_question, "question.csv")
        return redirect('/')

    return render_template('new_question.html', user_stories=questions, table_head=questions_head)


@app.route('/question/<int:story_id>/')
def route_list4(story_id):
    questions = data_handler.get_all_user_story("question.csv")
    questions_head = data_handler.get_data_header("question.csv")
    answers = data_handler.get_all_user_story("answer.csv")
    answers_head = data_handler.get_data_header("answer.csv")

    return render_template('display_question.html', questions=questions, questions_head=questions_head, answers=answers,
                           answers_head=answers_head, story_id=str(story_id))


@app.route('/question/<int:story_id>/edit', methods=['GET', 'POST'])
def route_list5(story_id):
    user_stories = data_handler.get_all_user_story("question.csv")
    table_head = data_handler.get_data_header("question.csv")
    if request.method == 'POST':
        edited_story = {}
        for key, value in user_stories[str(story_id)].items():
            edited_story[key] = value
        for key, value in request.form.items():
            edited_story[key] = value.replace('\n', '<br>').replace('\r', '')
        if user_stories[str(story_id)] == edited_story:
            return redirect('/question/' + str(story_id) + '/edit')
        user_stories[str(story_id)] = edited_story
        data_handler.write_all_story(user_stories, table_head, "question.csv")

        return redirect('/question/' + str(story_id) + '/')
    return render_template('update_question.html', user_stories=user_stories, table_head=table_head,
                           story_id=str(story_id))


@app.route('/question/<int:story_id>/new-answer/', methods=['GET', 'POST'])
def route_list6(story_id):
    answers_head = data_handler.get_data_header("answer.csv")
    if request.method == 'POST':
        answers = data_handler.get_all_user_story("answer.csv")
        max_id = util.get_max_id(answers)
        new_question = {answers_head[0]: max_id, answers_head[1]: str(round(time.time())),
                        answers_head[2]: '0', answers_head[3]: str(story_id)}
        for key, value in request.form.items():
            new_question[key] = value
        answers[max_id] = new_question
        data_handler.write_all_story(answers, answers_head, 'answer.csv')
        return redirect('/question/' + str(story_id) + '/')
    return render_template('new_answer.html', table_head=answers_head, story_id=story_id)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
