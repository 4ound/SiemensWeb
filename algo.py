import requests
import os

api_url = os.getenv("API_URL")


def get_tasks(login, token):
    url = api_url + '/task_list'
    js = {'verification': {'login': login, 'token': token}}
    r = requests.post(url, json=js)
    if r.status_code == requests.codes.ok:
        return r.json().get('tasks')
    else:
        return None


def get_task(login, token, task_id):
    url = api_url + '/get_task'
    js = {'verification': {'login': login, 'token': token},
          'task': {'id': task_id}}
    r = requests.post(url, json=js)
    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        return r.text


def assign_user(login, token, task_id, as_login):
    url = api_url + '/assign_user_to_task'
    js = {'verification': {'login': login, 'token': token},
          'task': {'id': task_id},
          'user': {'login': as_login}}
    r = requests.post(url, json=js)
    return r.text


def add_user(login, token, new_login, new_password, new_name):
    url = api_url + '/add_user'
    js = {'verification': {'login': login, 'token': token},
          'user': {'login': new_login, 'name': new_name, 'password': new_password}}
    r = requests.post(url, json=js)
    return r.text


def add_task(login, token, name, description, status):
    url = api_url + '/add_task'
    js = {'verification': {'login': login, 'token': token},
          'task': {'name': name, 'description': description, 'status': status}}
    r = requests.post(url, json=js)
    return r.text


def get_my_info(login, token):
    url = api_url + '/me'
    js = {'verification': {'login': login, 'token': token}}
    r = requests.post(url, json=js)
    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        return r.text


def update_my_info(login, token, new_login, name, password):
    url = api_url + '/update_user'
    js = {'verification': {'login': login, 'token': token},
          'user': {'login': new_login, 'name': name, 'password': password}}
    r = requests.post(url, json=js)
    return r.text
