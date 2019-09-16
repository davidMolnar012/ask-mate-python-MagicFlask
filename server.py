from flask import Flask, render_template, request, redirect, url_for

import data_handler

app = Flask(__name__)


@app.route('/')
def route_list1():
    user_stories, table_head = data_handler.get_all_user_story()

    return render_template('list.html', user_stories=user_stories, table_head=table_head)


@app.route('/list')
def route_list2():
    return redirect('/')


@app.route('/story', methods=['GET', 'POST'])
def route_list3():
    user_stories, table_head = data_handler.get_all_user_story()
    if request.method == 'POST':
        max_id = str(max([int(item) for item in user_stories.keys()]) + 1)
        new_story = {table_head[0]: max_id}
        for key, value in request.form.items():
            new_story[key] = value.replace('\n', '<br>').replace('\r', '')
        new_story[table_head[6]] = 'planning'
        data_handler.write_new_story(new_story)
        return redirect('/')

    return render_template('story.html', user_stories=user_stories, table_head=table_head)


@app.route('/story/<int:story_id>', methods=['GET', 'POST'])
def route_list4(story_id):
    user_stories, table_head = data_handler.get_all_user_story()
    if request.method == 'POST':
        edited_story = {table_head[0]: story_id}
        for key, value in request.form.items():
            edited_story[key] = value.replace('\n', '<br>').replace('\r', '')
        user_stories[str(story_id)] = edited_story
        data_handler.write_whole_story(user_stories)

        return redirect('/')
    return render_template('update.html', user_stories=user_stories, table_head=table_head, story_id=str(story_id))


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
