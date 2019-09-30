from flask import Flask, render_template, request, redirect

import data_manager

app = Flask(__name__)


@app.route('/')
def route_list1():
    latest_5_answers = data_manager.get_latest_answers(5)
    return render_template('index.html' , answers=latest_5_answers)


@app.route('/list')
def route_list2():
    answers = data_manager.get_latest_answers()
    return render_template('index.html', answers=answers)



if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
