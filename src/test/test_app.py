import sys
import os
import pytest

sys.path.insert(0, os.path.join(
    os.path.dirname(__file__), '..', 'main'))

import database
import models


@pytest.fixture
def test_db(tmp_path, monkeypatch):
    db_file = tmp_path / "test_tasks.db"
    monkeypatch.setattr(database, 'DB_PATH', str(db_file))
    database.init_db()
    return db_file


def test_create_task(test_db):
    models.create_task(
        'Buy groceries', 'Milk and eggs',
        'High', 'Personal', '2026-07-01', '10:00')
    tasks = models.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0]['title'] == 'Buy groceries'


def test_get_all_tasks_empty(test_db):
    tasks = models.get_all_tasks()
    assert tasks == []


def test_get_task_by_id(test_db):
    models.create_task(
        'Study Flask', '', 'Medium',
        'Study', '2026-07-02', '')
    tasks = models.get_all_tasks()
    task_id = tasks[0]['id']
    task = models.get_task_by_id(task_id)
    assert task['title'] == 'Study Flask'


def test_update_task(test_db):
    models.create_task(
        'Old title', '', 'Low',
        'General', '', '')
    tasks = models.get_all_tasks()
    task_id = tasks[0]['id']
    models.update_task(
        task_id, 'New title', '',
        'High', 'Work', '', '')
    updated = models.get_task_by_id(task_id)
    assert updated['title'] == 'New title'
    assert updated['priority'] == 'High'


def test_delete_task(test_db):
    models.create_task(
        'Task to delete', '', 'Low',
        'General', '', '')
    tasks = models.get_all_tasks()
    task_id = tasks[0]['id']
    models.delete_task(task_id)
    assert models.get_all_tasks() == []


def test_toggle_complete(test_db):
    models.create_task(
        'Toggle me', '', 'Medium',
        'General', '', '')
    tasks = models.get_all_tasks()
    task_id = tasks[0]['id']
    assert tasks[0]['completed'] == 0
    models.toggle_complete(task_id)
    task = models.get_task_by_id(task_id)
    assert task['completed'] == 1


def test_toggle_complete_twice(test_db):
    models.create_task(
        'Toggle twice', '', 'Medium',
        'General', '', '')
    tasks = models.get_all_tasks()
    task_id = tasks[0]['id']
    models.toggle_complete(task_id)
    models.toggle_complete(task_id)
    task = models.get_task_by_id(task_id)
    assert task['completed'] == 0


def test_search_tasks(test_db):
    models.create_task(
        'Buy milk', '', 'Low',
        'Personal', '', '')
    models.create_task(
        'Study Python', '', 'High',
        'Study', '', '')
    results = models.search_tasks('milk')
    assert len(results) == 1
    assert results[0]['title'] == 'Buy milk'


def test_search_no_results(test_db):
    models.create_task(
        'Buy milk', '', 'Low',
        'Personal', '', '')
    results = models.search_tasks('xyz')
    assert results == []


def test_filter_by_priority(test_db):
    models.create_task(
        'High task', '', 'High',
        'Work', '', '')
    models.create_task(
        'Low task', '', 'Low',
        'Work', '', '')
    results = models.filter_tasks(priority='High')
    assert len(results) == 1
    assert results[0]['priority'] == 'High'


def test_filter_by_category(test_db):
    models.create_task(
        'Work task', '', 'Medium',
        'Work', '', '')
    models.create_task(
        'Personal task', '', 'Medium',
        'Personal', '', '')
    results = models.filter_tasks(category='Work')
    assert len(results) == 1
    assert results[0]['category'] == 'Work'


def test_filter_completed(test_db):
    models.create_task(
        'Done task', '', 'Medium',
        'General', '', '')
    tasks = models.get_all_tasks()
    models.toggle_complete(tasks[0]['id'])
    results = models.filter_tasks(completed=1)
    assert len(results) == 1
    assert results[0]['completed'] == 1


def test_filter_by_date_range(test_db):
    models.create_task('Early task', '', 'Low',
                       'General', '2026-06-01', '')
    models.create_task('Mid task', '', 'Medium',
                       'General', '2026-06-15', '')
    models.create_task('Late task', '', 'High',
                       'General', '2026-06-30', '')
    results = models.filter_tasks(date_from='2026-06-10',
                                  date_to='2026-06-20')
    assert len(results) == 1
    assert results[0]['title'] == 'Mid task'


def test_filter_date_from_only(test_db):
    models.create_task('Old', '', 'Low',
                       'General', '2026-05-01', '')
    models.create_task('Recent', '', 'Low',
                       'General', '2026-07-01', '')
    results = models.filter_tasks(date_from='2026-06-01')
    assert len(results) == 1
    assert results[0]['title'] == 'Recent'


def test_filter_date_to_only(test_db):
    models.create_task('Old', '', 'Low',
                       'General', '2026-05-01', '')
    models.create_task('Future', '', 'Low',
                       'General', '2026-09-01', '')
    results = models.filter_tasks(date_to='2026-06-30')
    assert len(results) == 1
    assert results[0]['title'] == 'Old'


def test_reschedule_task(test_db):
    models.create_task('Reschedule me', '', 'Medium',
                       'Work', '2026-06-01', '09:00')
    tasks = models.get_all_tasks()
    task_id = tasks[0]['id']
    models.reschedule_task(task_id, '2026-06-20')
    updated = models.get_task_by_id(task_id)
    assert updated['due_date'] == '2026-06-20'


def test_reschedule_preserves_other_fields(test_db):
    models.create_task('Keep my data', 'desc', 'High',
                       'Study', '2026-06-01', '10:00')
    tasks = models.get_all_tasks()
    task_id = tasks[0]['id']
    models.reschedule_task(task_id, '2026-07-04')
    updated = models.get_task_by_id(task_id)
    assert updated['title']    == 'Keep my data'
    assert updated['priority'] == 'High'
    assert updated['due_time'] == '10:00'
    assert updated['due_date'] == '2026-07-04'
    def test_reschedule_nonexistent_task(test_db):
        result = models.reschedule_task(9999, '2026-08-01')
        assert result == False