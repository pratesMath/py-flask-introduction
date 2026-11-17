import pytest
import requests

BASE_URL = 'http://127.0.0.1:5000'
tasks = []

def test_create_task():
	# arrange
	new_task_data = {
		'title': 'Nova tarefa',
		'description': 'Descrição da nova tarefa'
	}
	# act
	response = requests.post(f'{BASE_URL}/tasks', json=new_task_data)

	response_json = response.json()
	# assert
	assert response.status_code == 201
	assert 'message' in response_json
	assert 'id' in response_json

	tasks.append(response_json['id'])

def test_get_tasks():
	# act
	response = requests.get(f'{BASE_URL}/tasks')
	response_json = response.json()
	# assert
	assert response.status_code == 200
	assert 'tasks' in response_json
	assert 'total' in response_json

def test_get_task_by_id():
	if tasks:
		# arrange
		task_id = tasks[0]
		# act
		response = requests.get(f'{BASE_URL}/tasks/{task_id}')
		response_json = response.json()
		# assert
		assert response.status_code == 200
		assert task_id == response_json['id']

def test_update_task_by_id():
	if tasks:
		# arrange
		task_id = tasks[0]
		payload = {
			'completed': True,
			'description': 'Nova descrição',
			'title': 'Título atualizado'
		}
		# act
		response = requests.put(f'{BASE_URL}/tasks/{task_id}', json=payload)
		response_json = response.json()
		# assert
		assert response.status_code == 200
		assert 'message' in response_json
		# act
		response = requests.get(f'{BASE_URL}/tasks/{task_id}')
		response_json = response.json()
		# assert
		assert response.status_code == 200
		assert response_json['title'] == payload['title']
		assert response_json['description'] == payload['description']
		assert response_json['completed'] == payload['completed']

def test_delete_task_by_id():
	if tasks:
		# arrange
		task_id = tasks[0]
		# act
		response = requests.delete(f'{BASE_URL}/tasks/{task_id}')
		# assert
		response.status_code == 200
		# act
		response = requests.get(f'{BASE_URL}/tasks/{task_id}')
		# assert
		assert response.status_code == 404
