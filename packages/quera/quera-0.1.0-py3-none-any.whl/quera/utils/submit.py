import requests
from getpass import getpass

from quera.utils.cache import cache

JUDGE_API = 'https://quera.org/judge_api/apikey-judge/'


def get_apikey() -> str:
    if 'apikey' not in cache:
        print('Enter you APIKey please:')
        cache['apikey'] = getpass('Quera APIKey: ')
    return cache['apikey']


def set_problem_id(problem_id: int):
    cache['problem_id'] = problem_id


def get_problem_id() -> int:
    if 'problem_id' not in cache:
        raise Exception('run `set_problem_id(...)` function before calling this one.')
    return cache['problem_id']


def set_file_type_id(file_type_id: int):
    cache['file_type_id'] = file_type_id


def get_file_type_id() -> int:
    if 'file_type_id' not in cache:
        raise Exception('run `set_file_type_id(...)` function before calling this one.')
    return cache['file_type_id']


def submit(*, submitting_file_name: str = 'result.zip', api: str = JUDGE_API):
    problem_id = get_problem_id()
    file_type_id = get_file_type_id()

    with open(submitting_file_name, 'rb') as result:
        response = requests.post(
            api,
            files={'file': result},
            data={'problem_id': problem_id, 'file_type': file_type_id},
            headers={'Judge-APIKey': get_apikey()}
        )
        if response.status_code != 201:
            print(f'Error - {response.status_code}: ', response.content.decode())
        else:
            print('Submitted to Quera Successfully')
