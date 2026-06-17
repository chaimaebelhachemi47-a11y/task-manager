import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import (Flask, render_template, request,
                   redirect, url_for, jsonify)
from database import init_db
from models import (create_task, get_all_tasks, get_task_by_id,
                    update_task, delete_task, toggle_complete,
                    search_tasks, filter_tasks, reschedule_task)

app = Flask(__name__)

with app.app_context():
    init_db()


@app.route('/')
def index():
    tasks = get_all_tasks()
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        if not title:
            return render_template('add_task.html',
                                   error='Title is required.')
        create_task(
            title,
            request.form.get('description', ''),
            request.form.get('priority', 'Medium'),
            request.form.get('category', 'General'),
            request.form.get('due_date', ''),
            request.form.get('due_time', '')
        )
        return redirect(url_for('index'))
    return render_template('add_task.html')


@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = get_task_by_id(task_id)
    if not task:
        return redirect(url_for('index'))
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        if not title:
            return render_template('edit_task.html',
                                   task=task,
                                   error='Title is required.')
        update_task(
            task_id,
            title,
            request.form.get('description', ''),
            request.form.get('priority', 'Medium'),
            request.form.get('category', 'General'),
            request.form.get('due_date', ''),
            request.form.get('due_time', '')
        )
        return redirect(url_for('index'))
    return render_template('edit_task.html', task=task)


@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task_route(task_id):
    delete_task(task_id)
    return redirect(url_for('index'))


@app.route('/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    toggle_complete(task_id)
    return redirect(url_for('index'))


@app.route('/reschedule/<int:task_id>', methods=['POST'])
def reschedule(task_id):
    data = request.get_json()
    new_date = data.get('due_date', '')
    if not new_date:
        return jsonify({'status': 'error', 'msg': 'no date'}), 400
    success = reschedule_task(task_id, new_date)
    if not success:
        return jsonify({'status': 'error', 'msg': 'task not found'}), 404
    return jsonify({'status': 'ok'})

@app.route('/search')
def search():
    keyword = request.args.get('q', '')
    tasks = search_tasks(keyword) if keyword else []
    return render_template('index.html',
                           tasks=tasks,
                           search_query=keyword)


@app.route('/filter')
def filter_view():
    category  = request.args.get('category', '')
    priority  = request.args.get('priority', '')
    completed = request.args.get('completed', '')
    date_from = request.args.get('date_from', '')
    date_to   = request.args.get('date_to', '')

    completed_val = None
    if completed == '1':
        completed_val = 1
    elif completed == '0':
        completed_val = 0

    tasks = filter_tasks(
        category=category  or None,
        priority=priority  or None,
        completed=completed_val,
        date_from=date_from or None,
        date_to=date_to    or None,
    )
    return render_template('index.html', tasks=tasks,
                           filter_category=category,
                           filter_priority=priority,
                           filter_completed=completed,
                           filter_date_from=date_from,
                           filter_date_to=date_to)


@app.route('/calendar')
def calendar_view():
    tasks = get_all_tasks()
    return render_template('calendar.html', tasks=tasks)


if __name__ == '__main__':
    app.run(debug=True)