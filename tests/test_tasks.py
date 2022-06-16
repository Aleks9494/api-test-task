import requests


def test_show_task(task):
    url = 'http://localhost:5000/api/tasks/' + f'{task.id}'
    response = requests.get(url)

    assert response.status_code == 200
    assert response.json()['title'] == 'Task # 1'


def test_add_task():
    data = {'title': 'Task # 2', 'body': 'Body of task # 2', 'date_to_do': '2022-07-28'}
    response = requests.post('http://localhost:5000/api/tasks', json=data)

    assert response.status_code == 200
    assert response.json()['title'] == 'Task # 2'


def test_show_tasks():
    response = requests.get('http://localhost:5000/api/tasks')

    assert response.status_code == 200
    assert response.json()[1]['title'] == 'Task # 2'
    assert response.json()[0]['title'] == 'Task # 1'
    assert len(response.json()) == 2


def test_update_task(task):
    url = 'http://localhost:5000/api/tasks/' + f'{task.id}'
    data = {'mark': 'True'}
    response = requests.put(url, json=data)

    assert response.status_code == 200
    assert response.json()['title'] == 'Task # 1'
    assert response.json()['mark'] == True


def test_delete_task(task):
    url = 'http://localhost:5000/api/tasks/' + f'{task.id}'
    response = requests.delete(url)

    assert response.status_code == 200
    assert response.json()['message'] == f'Task with id = {task.id} deleted'
