from flask import Flask, session, redirect, request, render_template, abort, url_for
import algo
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    login = session.get('login', None)
    if login is None:
        return redirect('{}/login?redirect={}new'.format(algo.api_url, request.host_url))
    else:
        tasks = algo.get_tasks(session.get('login'), session.get('token'))
        return render_template('index.html', tasks=tasks)


@app.route('/task/<int:task_id>', methods=['GET', 'POST'])
def view_task(task_id):
    error = None
    if request.method == 'POST':
        code = algo.assign_user(session.get('login'), session.get('token'), task_id, request.form['login'])
        if code != 'OK':
            error = code

    task = algo.get_task(session.get('login'), session.get('token'), task_id)
    if type(task) is not dict:
        if error is None:
            error, task = task, error
        else:
            error = error + '\n' + task

    return render_template('task.html', task=task, error=error)


@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    error = None
    if request.method == 'POST':
        code = algo.add_user(session.get('login'), session.get('token'), request.form['login'],
                             request.form['password'], request.form['name'])
        if code != 'OK':
            error = code
        else:
            return redirect(url_for('index'))

    return render_template('user.html', error=error)


@app.route('/new_task', methods=['GET', 'POST'])
def new_task():
    error = None
    if request.method == 'POST':
        code = algo.add_task(session.get('login'), session.get('token'), request.form['name'],
                             request.form['description'], request.form['status'])
        if code != 'OK':
            error = code
        else:
            return redirect(url_for('index'))

    return render_template('new_task.html', error=error)


@app.route('/me', methods=['GET', 'POST'])
def me():
    error = None
    if request.method == 'POST':
        code = algo.update_my_info(session.get('login'), session.get('token'), request.form['login'],
                                   request.form['name'], request.form['password'])
        if code != 'OK':
            error = code
        else:
            session['login'] = request.form['login']
            return redirect(url_for('index'))
    else:
        code = algo.get_my_info(session.get('login'), session.get('token'))
        if type(code) is not dict:
            error = code

    return render_template('me.html', error=error, code=code)


@app.route('/new')
def new_auth():
    login = request.args.get('login')
    token = request.args.get('token')
    if login is None or token is None:
        abort(500)

    session['login'] = login
    session['token'] = token

    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('login')
    session.pop('token')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4444)
